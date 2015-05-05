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
runtime = 1.0
inject = 25e-10
simdt = 5e-5
FaradayConst = 96845.34

def makePlot( cell ):
    fig = plt.figure( figsize = ( 10, 12 ) )
    chans = ['hd', 'kdr', 'na3', 'nax', 'kap', 'kad']
    compts = cell.compartments
    epos = cell.electrotonicDistanceFromSoma
    gpos = cell.geometricalDistanceFromSoma
    combo = zip( gpos, compts )
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

def main():
    cm = ChannelML( {'temperature': 32 })
    cm.readChannelMLFromFile( 'CA1_migliore_reference/hd.xml' )
    cm.readChannelMLFromFile( 'CA1_migliore_reference/kap.xml' )
    cm.readChannelMLFromFile( 'CA1_migliore_reference/kad.xml' )
    cm.readChannelMLFromFile( 'CA1_migliore_reference/kdr.xml' )
    cm.readChannelMLFromFile( 'CA1_migliore_reference/na3.xml' )
    cm.readChannelMLFromFile( 'CA1_migliore_reference/nax.xml' )
    if ( len( sys.argv ) < 2 ):
        print "Usage: ", sys.argv[0], " filename"
        return

    # filename = "./Bhavika_swcplusnmlfiles/preliminarily corrected nmlfiles/ascoli+buzsaki/valid/" + sys.argv[1]
    filename = sys.argv[1]
    moose.Neutral( '/model' )
    # Load in the swc file.
    cell = moose.loadModel( filename, '/model/ca1' )

    for i in moose.wildcardFind( '/library/##' ):
        i.tick = -1

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
    for i in range( 8 ):
        moose.setClock( i, simdt )
    hsolve = moose.HSolve( '/model/ca1/hsolve' )
    hsolve.dt = simdt
    hsolve.target = '/model/ca1/soma'
    '''
    '''
    moose.reinit()
    compts = moose.wildcardFind( "/model/ca1/#[ISA=CompartmentBase]" )
    compts[0].inject = inject
    startt = time.time()
    moose.start(1)
    print 'tot time = ', time.time() - startt
    sys.exit()
    makePlot( cell[0] )

    # Now we set up the display
    moose.le( '/model/ca1/soma' )
    soma = moose.element( '/model/ca1/soma' )
    kap = moose.element( '/model/ca1/soma/kap' )

    graphs = moose.Neutral( '/graphs' )
    vtab = moose.Table( '/graphs/vtab' )
    moose.connect( vtab, 'requestOut', soma, 'getVm' )
    kaptab = moose.Table( '/graphs/kaptab' )
    moose.connect( kaptab, 'requestOut', kap, 'getGk' )

    compts = moose.wildcardFind( "/model/ca1/#[ISA=CompartmentBase]" )
    '''
    for i in compts:
        if moose.exists( i.path + '/Na' ):
            print i.path, moose.element( i.path + '/Na' ).Gbar, \
                moose.element( i.path + '/K_DR' ).Gbar, \
                i.Rm, i.Ra, i.Cm
    '''
    '''
    Na = moose.wildcardFind( '/model/ca1/#/Na#' )
    print Na
    Na2 = []
    for i in compts:
        if ( moose.exists( i.path + '/NaF2' ) ):
            Na2.append(  moose.element( i.path + '/NaF2' ) )
        if ( moose.exists( i.path + '/NaPF_SS' ) ):
            Na2.append(  moose.element( i.path + '/NaPF_SS' ) )
    ecomptPath = map( lambda x : x.path, compts )
    print "Na placed in ", len( Na ), len( Na2 ),  " out of ", len( compts ), " compts."
    '''
    compts[0].inject = inject
    ecomptPath = map( lambda x : x.path, compts )

    # Graphics stuff here.
    app = QtGui.QApplication(sys.argv)
    morphology = moogli.read_morphology_from_moose(name = "", path = "/model/ca1")
    morphology.create_group( "group_all", ecomptPath, -0.08, 0.02, \
            [0.0, 0.0, 1.0, 1.0], [1.0, 0.0, 0.0, 0.1] ) 

    viewer = moogli.DynamicMorphologyViewerWidget(morphology)
    def callback( morphology, viewer ):
        moose.start( frameRunTime )
        Vm = map( lambda x: moose.element( x ).Vm, compts )
        morphology.set_color( "group_all", Vm )
        currTime = moose.element( '/clock' ).currentTime
        #print currTime, compts[0].Vm
        if ( currTime < runtime ):
            return True
        return False

    viewer.set_callback( callback, idletime = 0 )
    viewer.showMaximized()
    viewer.show()
    app.exec_()
    t = numpy.arange( 0, runtime, vtab.dt )
    fig = plt.figure()
    p1 = fig.add_subplot(311)
    p2 = fig.add_subplot(312)
    p2.plot( t,  vtab.vector, label = 'Vm Soma' )
    p2.legend()
    p3 = fig.add_subplot(313)
    p3.plot( t, kaptab.vector, label = 'kap Soma' )
    p3.legend()
    plt.show()

if __name__ == '__main__':
    main()
