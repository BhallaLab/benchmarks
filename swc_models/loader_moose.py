"""loader_moose.py: 

    Load a SWC file in MOOSE.
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import numpy as np
import pylab
import moose
import time
import moose.utils as mu
from moose import neuroml
from PyQt4 import Qt, QtCore, QtGui
import matplotlib.pyplot as plt
import sys
import os
from moose.neuroml.ChannelML import ChannelML
from _profile import dbEntry

PI = 3.14159265359
frameRunTime = 0.001
FaradayConst = 96845.34
modelName = None
simulator = 'moose'
ncompts = 0
nchans = 0
_args = None
_records = {}


def makePlot( cell ):
    fig = plt.figure( figsize = ( 10, 12 ) )
    chans = ['hd', 'kdr', 'na3', 'nax', 'kap', 'kad']
    compts = cell.compartments
    epos = cell.electrotonicDistanceFromSoma
    gpos = cell.geometricalDistanceFromSoma
    combo = list(zip( gpos, compts ))
    #combo.sort( key=lambda c:c[1].x)
    combo.sort( key= lambda c:c[0] )
    for i in chans:
        x = []
        y = []
        for j in combo:
            area = j[1].length * j[1].diameter * PI
            #x.append( j[1].x )
            x.append( j[0] )
            if moose.exists( j[1].path + '/' + i ):
                elm = moose.element( j[1].path + '/' + i )
                y.append( elm.Gbar / area )
            else:
                y.append( 0.0 )
        pylab.plot( x, y, '-bo', label = i )
        pylab.legend()
        pylab.show()

def saveData( outfile ):
    clock = moose.Clock('/clock')
    yvec = None
    for k in _records:
        if "soma" in k: yvec = _records[k].vector
    xvec = np.linspace(0, clock.currentTime, len(yvec))
    with open(outfile, "wb") as f:
        f.write("%s,%s\n" % ('time', 'soma'))
        for i, t in enumerate(xvec):
            f.write("%s,%s\n" % (t, yvec[i]))
    mu.info("[INFO] Done writing to file %s" % outfile)


def loadModel(filename, args):
    """Load the model and insert channels """
    global modelName
    global nchans, ncompts

    moose.Neutral( '/model' )
    # Load in the swc file.
    modelName = filename.split('/')[-1]
    print("[INFO] Opening model file: %s" % modelName)
    cell = moose.loadModel( filename, '/model/{}'.format(modelName))

    if args.insert_channels:
        print("[INFO] Adding channels")
        cm = ChannelML( {'temperature': 32 })
        cm.readChannelMLFromFile( 'hd.xml' )
        cm.readChannelMLFromFile( 'kap.xml' )
        cm.readChannelMLFromFile( 'kad.xml' )
        cm.readChannelMLFromFile( 'kdr.xml' )
        cm.readChannelMLFromFile( 'na3.xml' )
        cm.readChannelMLFromFile( 'nax.xml' )

        chanDistrib = [ \
            "EM", "#", "-70e-3", \
            "initVm", "#", "-70e-3", \
            "RM", "#", "2.8", \
            "CM", "#", "0.01", \
            "RA", "#", "1.5", \
            "RA", "#axon#", "0.5" ]

        chanDistrib += [
            "hd", "#dend#,#apical#", "5e-2*(1+(r*3e4))", \
            "kdr", "#", "100", \
            "na3", "#soma#,#dend#,#apical#", "250", \
            "nax", "#axon#", "1250", \
            "kap", "#axon#,#soma#", "300", \
            "kap", "#dend#,#apical#", "150*(1+sign(100-r*1e6)) * (1+(r*1e4))", \
            "kad", "#dend#,#apical#", "150*(1+sign(r*1e6-100))*(1+r*1e4)", \
            ]
        cell[0].channelDistribution = chanDistrib
        cell[0].parseChanDistrib()
        moose.showfields( cell[0] )

    if args.plots:
        print("[INFO] Plotting is ON")
        #makePlot( cell[0] )
        # Now we set up the display
        moose.le( '/model/%s/soma'%modelName )
        soma = moose.element( '/model/%s/soma'%modelName )
        assert soma

        graphs = moose.Neutral( '/graphs' )
        compts = moose.wildcardFind( "/model/%s/#[ISA=CompartmentBase]"%modelName )
        setupStimuls(compts[0])
        for compt in compts:
            vtab = moose.Table( '%s/vm' % compt.path )
            moose.connect( vtab, 'requestOut', compt, 'getVm' )
            _records[compt.path] = vtab

    for i in range( 8 ):
        moose.setClock( i, args.sim_dt )

    hsolve = moose.HSolve( '/model/%s/hsolve' % modelName )
    hsolve.dt = args.sim_dt
    hsolve.target = '/model/%s/soma ' % modelName
    moose.reinit()

def setupStimuls(compt):
    global _args
    command = moose.PulseGen('%s/command' % compt.path)
    print("[INFO] Injecting %s (Amps) of current" % _args.inject)
    command.level[0] = _args.inject
    command.delay[0] = 0
    command.width[0] = _args.sim_time
    moose.connect(command, 'output', compt, 'injectMsg')

def plots(filter='soma'):
    global _records
    global _args
    if not _args.plots:
        return 
    else:
        toPlot = []
        tables = {}
        for k in _records:
            if filter in k:
                toPlot.append(k)
        for k in toPlot:
            tables[k] = _records[k]
        mu.plotRecords(tables, outfile=_args.plots)

def main(args):
    global _args
    _args = args
    global ncompts, nchans
    loadModel(args.swc_file, args)
    moose.reinit()
    compts = moose.wildcardFind( "/model/%s/#[ISA=CompartmentBase]" % modelName )
    ncompts = len(compts)
    startt = time.time()
    moose.start(args.sim_time)
    t = time.time() - startt
    dbEntry(simulator='moose'
            , model_name=args.swc_file
            , no_of_compartments=ncompts
            , no_of_channels=nchans
            , simtime=args.sim_time
            , runtime=t
            , dt=args.sim_dt
            )

    saveData(outfile="_data/moose.csv")
