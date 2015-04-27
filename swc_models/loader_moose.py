#!/usr/bin/env python

import moogli
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

PI = 3.14159265359
frameRunTime = 0.001
inject = 25e-10
FaradayConst = 96845.34
modelName = None

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
                "RA", "#axon#", "0.5", \

                "hd", "#dend#,#apical#", "5e-2*(1+(r*3e4))", \
                "kdr", "#", "100", \
                "na3", "#soma#,#dend#,#apical#", "250", \
                "nax", "#axon#", "1250", \
                "kap", "#axon#,#soma#", "300", \
                "kap", "#dend#,#apical#", "150*(1+sign(100-r*1e6)) * (1+(r*1e4))", \
                "kad", "#dend#,#apical#", "150*(1+sign(r*1e6-100))*(1+r*1e4)", \
                ]
        moose.showfields( cell[0] )
        cell[0].channelDistribution = chanDistrib
        cell[0].parseChanDistrib()

    if args.plots:
        print("[INFO] Plotting is ON")
        makePlot( cell[0] )
        # Now we set up the display
        moose.le( '/model/%s/soma'%modelName )
        soma = moose.element( '/model/%s/soma'%modelName )
        kap = moose.element( '/model/%s/soma/kap'%modelName )

        graphs = moose.Neutral( '/graphs' )
        vtab = moose.Table( '/graphs/vtab' )
        moose.connect( vtab, 'requestOut', soma, 'getVm' )
        kaptab = moose.Table( '/graphs/kaptab' )
        moose.connect( kaptab, 'requestOut', kap, 'getGk' )

        compts = moose.wildcardFind( "/model/%s/#[ISA=CompartmentBase]"%modelName )
        compts[0].inject = inject
        ecomptPath = [x.path for x in compts]

        t = numpy.arange( 0, args.sim_time, vtab.dt )
        fig = plt.figure()
        p1 = fig.add_subplot(311)
        p2 = fig.add_subplot(312)
        p2.plot( t,  vtab.vector, label = 'Vm Soma' )
        p2.legend()
        p3 = fig.add_subplot(313)
        p3.plot( t, kaptab.vector, label = 'kap Soma' )
        p3.legend()
        plt.show()

    for i in range( 8 ):
        moose.setClock( i, args.sim_dt )

    hsolve = moose.HSolve( '/model/%s/hsolve' % modelName )
    hsolve.dt = args.sim_dt
    hsolve.target = '/model/%s/soma' % modelName
    moose.reinit()
    compts = moose.wildcardFind( "/model/%s/#[ISA=CompartmentBase]" % modelName )
    compts[0].inject = inject
    startt = time.time()
    moose.start(args.sim_time)
    print('tot time = {}'.format(time.time() - startt))
    sys.exit()
