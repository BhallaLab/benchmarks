########################################################################
# This program is copyright (c) Upinder S. Bhalla, NCBS, 2015.
# It is licenced under the GPL 2.1 or higher.
# There is no warranty of any kind. You are welcome to make copies under 
# the provisions of the GPL.
# This programme illustrates building a panel of multiscale models to
# test neuronal plasticity in different contexts.
########################################################################
#import moogli
import numpy
import time
import pylab
from moose import neuroml
from PyQt4 import Qt, QtCore, QtGui
import matplotlib.pyplot as plt
import sys
import moose
import os
from moose.neuroml.ChannelML import ChannelML
sys.path.append(os.path.join(os.environ['HOME'], 'moose3.0.1/Demos/util'))
import rdesigneur as rd

PI = 3.14159265359
frameRunTime = 0.001
runtime = 0.2
inject = 1e-9
simdt = 5e-5
FaradayConst = 96845.34
useGssa = True
combineSegments = False
#elecFileNames = ( "ca1_minimal.p", )
#elecFileNames = ( "ca1_minimal.p", "h10.CNG.swc", "CA1.morph.xml", "VHC-neuron.CNG.swc" )
elecFileNames = ( "VHC-neuron.CNG.swc", )
synSpineList = []
synDendList = []

def buildRdesigneur():
    ##################################################################
    # Here we define which prototypes are to be loaded in to the system.
    # Each specification has the format
    # source [localName]
    # source can be any of
    # filename.extension,   # Identify type of file by extension, load it.
    # function(),           # func( name ) builds object of specified name
    # file.py:function() ,  # load Python file, run function(name) in it.
    # moose.Classname       # Make obj moose.Classname, assign to name.
    # path                  # Already loaded into library or on path.
    # After loading the prototypes, there should be an object called 'name'
    # in the library.
    ##################################################################
    chanProto = [
        ['./chans/hd.xml'], \
        ['./chans/kap.xml'], \
        ['./chans/kad.xml'], \
        ['./chans/kdr.xml'], \
        ['./chans/na3.xml'], \
        ['./chans/nax.xml'], \
        ['./chans/CaConc.xml'], \
        ['./chans/Ca.xml'], \
        ['./chans/NMDA.xml'], \
        ['./chans/Glu.xml'] \
    ]
    spineProto = [ \
        ['makeSpineProto()', 'spine' ]
    ]

    ##################################################################
    # Here we define what goes where, and any parameters. Each distribution
    # has the format
    # protoName, path, field, expr, [field, expr]...
    # where 
    #   protoName identifies the prototype to be placed on the cell
    #   path is a MOOSE wildcard path specifying where to put things
    #   field is the field to assign.
    #   expr is a math expression to define field value. This uses the
    #     muParser. Built-in variables are p, g, L, len, dia.
    #     The muParser provides most math functions, and the Heaviside 
    #     function H(x) = 1 for x > 0 is also provided.
    ##################################################################
    passiveDistrib = [ 
            [ ".", "#", "RM", "2.8", "CM", "0.01", "RA", "1.5",  \
                "Em", "-58e-3", "initVm", "-65e-3" ], \
            [ ".", "#axon#", "RA", "0.5" ] \
        ]
    chanDistrib = [ \
            ["hd", "#dend#,#apical#", "Gbar", "5e-2*(1+(p*3e4))" ], \
            ["kdr", "#", "Gbar", "p<50 ? 500 : 100" ], \
            ["na3", "#soma#,#dend#,#apical#", "Gbar", "250" ], \
            ["nax", "#soma#,#axon#", "Gbar", "1250" ], \
            ["kap", "#axon#,#soma#", "Gbar", "300" ], \
            ["kap", "#dend#,#apical#", "Gbar", \
                "300*(H(100-p*1e6)) * (1+(p*1e4))" ], \
            ["Ca_conc", "#dend#,#apical#", "tau", "0.0133" ], \
            ["kad", "#soma#,#dend#,#apical#", "Gbar", \
                "300*H(p - 100e-6)*(1+p*1e4)" ], \
            ["Ca", "#dend#,#apical#", "Gbar", "50" ]
        ]
    spineDistrib = [ \
            ["spine", '#apical#', "spineSpacing", "H(p - 400e-6)*H(800e-6 - p)*10e-6", \
                "spineSpacingDistrib", "5e-6", \
                "angle", "0", \
                "angleDistrib", str( 2*PI ), \
                "size", "1", \
                "sizeDistrib", "0.5" ] \
        ]

    ######################################################################
    # Having defined everything, now to create the rdesigneur and proceed
    # with creating the model.
    ######################################################################
    

    rdes = rd.rdesigneur(
        useGssa = useGssa, \
        combineSegments = combineSegments, \
        stealCellFromLibrary = True, \
        passiveDistrib = passiveDistrib, \
        spineDistrib = spineDistrib, \
        chanDistrib = chanDistrib, \
        spineProto = spineProto, \
        chanProto = chanProto
    )

    return rdes

def buildPlots( rdes ):
    if not moose.exists( '/graphs' ):
        graphs = moose.Neutral( '/graphs' )
    somaVmTab = moose.Table( '/graphs/somaVmTab' )
    moose.connect( somaVmTab, 'requestOut', rdes.soma, 'getVm' )
    spineList = rdes.elecid.spinesFromExpression[ "# 1" ]
    comptList = rdes.elecid.compartments
    path = comptList[100].path + "/Ca_conc"
    if moose.exists( path ):
        dendCaTab = moose.Table( '/graphs/dendCaTab' )
        moose.connect( dendCaTab, 'requestOut', path, 'getCa' )
    eSpineVmTab = moose.Table( '/graphs/eSpineVmTab' )
    moose.connect( eSpineVmTab, 'requestOut', spineList[1], 'getVm' )
    somaNaGkTab = moose.Table( '/graphs/somaNaGkTab' )
    path = rdes.soma.path + "/na3"
    moose.connect( somaNaGkTab, 'requestOut', path, 'getGk' )

def saveAndClearPlots( name ):
    print('saveAndClearPlots( ', name, ' )')
    for i in moose.wildcardFind( "/graphs/#" ):
        #print i
        #plot stuff
        i.xplot( name + '.xplot', i.name )
    moose.delete( "/graphs" )

def main():
    global synSpineList 
    global synDendList 
    numpy.random.seed( 1234 )
    rdes = buildRdesigneur()
    for i in elecFileNames:
        print(i)
        rdes.cellProtoList = [ ['./cells/' + i, 'elec'] ]
        rdes.buildModel( '/model' )
        rdes.soma.inject = inject
        assert( moose.exists( '/model' ) )
        synSpineList = moose.wildcardFind( "/model/elec/#head#/glu,/model/elec/#head#/NMDA" )
        temp = set( moose.wildcardFind( "/model/elec/#/glu,/model/elec/#/NMDA" ) )
        synDendList = list( temp - set( synSpineList ) )
        print("[INFO] reinitialzing")
        moose.reinit()
        buildPlots( rdes )
        # Run for baseline, tetanus, and post-tetanic settling time 
        t1 = time.time()
        moose.start( runtime )
        print('runtime = ', runtime, '; real time = ', time.time() - t1)

        saveAndClearPlots( "bigElec" )
        moose.delete( '/model' )
        rdes.elecid = moose.element( '/' )

if __name__ == '__main__':
    main()
