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

import numpy
import pylab
import moose
import time
from moose import neuroml
from PyQt4 import Qt, QtCore, QtGui
import matplotlib.pyplot as plt
import sys
import os
from moose.neuroml.ChannelML import ChannelML
from _profile import dbEntry

PI = 3.14159265359
frameRunTime = 0.001
inject = 25e-10
FaradayConst = 96845.34
modelName = None
simulator = 'moose'
ncompts = 0
nchans = 0
_args = None

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

def loadModel(filename, args):
    """Load the model and insert channels """
    global modelName
    global nchans, ncompts

    moose.Neutral( '/model' )
    # Load in the swc file.
    modelName = filename.split('/')[-1]
    print("[INFO] Opening model file: %s" % modelName)
    cell = moose.loadModel( filename, '/model/{}'.format(modelName))

    for i in moose.wildcardFind( '/library/##' ):
        i.tick = -1

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
                "EM", "#", "-58e-3", \
                "initVm", "#", "-65e-3", \
                "RM", "#", "2.8", \
                "CM", "#", "0.01", \
                "RA", "#", "1.5", \
                ] + [x.replace('*', '#') for x in args.insert_channels]

        moose.showfields( cell[0] )
        cell[0].channelDistribution = chanDistrib
        cell[0].parseChanDistrib()

    if args.plots:
        print("[INFO] Plotting is ON")
        #makePlot( cell[0] )
        # Now we set up the display
        moose.le( '/model/%s/soma'%modelName )
        soma = moose.element( '/model/%s/soma'%modelName )

        graphs = moose.Neutral( '/graphs' )
        vtab = moose.Table( '/graphs/vtab' )
        moose.connect( vtab, 'requestOut', soma, 'getVm' )

        compts = moose.wildcardFind( "/model/%s/#[ISA=CompartmentBase]"%modelName )
        compts[0].inject = inject
        ecomptPath = [x.path for x in compts]
    for i in range( 8 ):
        moose.setClock( i, args.sim_dt )

    hsolve = moose.HSolve( '/model/%s/hsolve' % modelName )
    hsolve.dt = args.sim_dt
    hsolve.target = '/model/%s/soma' % modelName

def plots():
    global _args
    vtab = moose.Table('/graphs/vtab')
    t = numpy.arange( 0, _args.sim_time, vtab.dt )
    fig = plt.figure()
    #assert len(t) == len(vtab.vector), "%s ?= %s" % (len(t), len(vtab.vector))
    plt.plot(t, vtab.vector[0:-1], label = 'Vm Soma' )
    plt.legend()
    if not _args.plots:
        return 
    else:
        print("[INFO] Saving plots to %s" % _args.plots)
        plt.savefig(_args.plots)
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

    plots()
