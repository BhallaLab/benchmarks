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
sys.path.append('/opt/moose/Demos/util')
import rdesigneur as rd
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
    assert clock
    yvec = None
    for k in _records:
        if "soma" in k: 
            yvec = _records[k].vector
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

    # Load in the swc file.
    modelName = "elec"
    cellProto = [ ( filename, modelName ) ]

    passiveDistrib = []
    chanDistrib = []
    if args.insert_channels:
        chanProto = [
                ['./hd.xml'], 
                ['./kap.xml'], 
                ['./kad.xml'], 
                ['./kdr.xml'], 
                ['./na3.xml'], 
                ['./nax.xml'], 
                #['./Ca.xml'], 
                #['./NMDA.xml'], 
                #['./Glu.xml'] 
                ]

        passiveDistrib = [ 
                [ ".", "#", "RM", "2.8", "CM", "0.01", "RA", "1.5",  
                    "Em", "-58e-3", "initVm", "-65e-3" ], 
                [ ".", "#axon#", "RA", "0.5" ] 
                ]

        chanDistrib = [ ['hd', '#dend#,#apical#', 'Gbar', '5e-2*(1+(p*3e4))']
                , ['kdr', '#', 'Gbar', '100']
                , ['na3', '#soma#,#dend#,#apical#', 'Gbar', '250']
                , ['nax', '#axon#', 'Gbar', '1250']
                , ['kap', '#axon#,#soma#', 'Gbar', '300']
                , ['kap', '#dend#,#apical#', 'Gbar', '150*(1+sign(100-p*1e6)) * (1+(p*1e4))']
                , ['kad', '#dend#,#apical#', 'Gbar', '150*(1+sign(p*1e6-100))*(1+p*1e4)']
                ]

    rdes = rd.rdesigneur( cellProto = cellProto
            , combineSegments = True
            , passiveDistrib = passiveDistrib
            , chanProto = chanProto
            , chanDistrib = chanDistrib
            )

    rdes.buildModel('/model')

    chans = moose.wildcardFind("/model/elec/##[TYPE=HHChannel]")
    print("Total channels found %s" % len(chans))
    #assert len(chans) > 0

    compts = moose.wildcardFind( "/model/%s/#[ISA=CompartmentBase]"%modelName )
    setupStimuls( compts[0] )

    for compt in compts:
        vtab = moose.Table( '%s/vm' % compt.path )
        moose.connect( vtab, 'requestOut', compt, 'getVm' )
        _records[compt.path] = vtab

def setupStimuls(compt):
    global _args
    command = moose.PulseGen('%s/command' % compt.path)
    print("[INFO] Injecting {} Amps into {} for {} seconds".format(
        _args.inject
        , compt.path
        , _args.sim_time)
        )
    command.level[0] = _args.inject
    command.delay[0] = 0
    command.width[0] = _args.sim_time
    m = moose.connect(command, 'output', compt, 'injectMsg')

def plots(filter='soma'):
    global _records
    global _args
    toPlot = []
    tables = {}
    for k in _records:
        if filter in k:
            toPlot.append(k)
    for k in toPlot:
        tables[k] = _records[k]
    mu.plotRecords(tables, subplot=True) #, outfile=_args.plots)
    plt.show()

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
