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


# Global variable to log query to database.
db_query_ = {}

PI = 3.14159265359
frameRunTime = 0.001
FaradayConst = 96845.34
modelName = None
simulator = 'moose'
ncompts = 0
nchans = 0
_args = None
_records = {}

import logging
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='moose.log',
    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
_logger = logging.getLogger('')

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
    _logger.debug("Done writing to file %s" % outfile)


def loadModel(filename, args):
    """Load the model and insert channels """
    global modelName
    global nchans, ncompts

    # Load in the swc file.
    modelName = "elec"
    cellProto = [ ( filename, modelName ) ]
    chanProto = [
            ['./chans/hd.xml'], 
            ['./chans/kap.xml'], 
            ['./chans/kad.xml'], 
            ['./chans/kdr.xml'], 
            ['./chans/na3.xml'], 
            ['./chans/nax.xml'], 
            ]

    passiveDistrib = [ 
            [ ".", "#", "RM", "2.8", "CM", "0.01", "RA", "1.5",  
                "Em", "-58e-3", "initVm", "-65e-3" ]
            , [ ".", "#axon#", "RA", "0.5" ] 
            ]
    chanDistrib = [
            [  "na3", "#", "Gbar", "1200" ]
            , [ "kap", "#", "Gbar", "360" ]
            ]

    rdes = rd.rdesigneur( cellProto = cellProto
            , combineSegments = True
            , passiveDistrib = passiveDistrib
            , chanProto = chanProto
            , chanDistrib = chanDistrib
            )

    rdes.buildModel('/model')

    compts = moose.wildcardFind( "/model/%s/#[ISA=CompartmentBase]"%modelName )
    setupStimuls( compts[0] )

    for compt in compts:
        vtab = moose.Table( '%s/vm' % compt.path )
        moose.connect( vtab, 'requestOut', compt, 'getVm' )
        _records[compt.path] = vtab

    nchans  = len(set([x.path for x in
        moose.wildcardFind('/model/elec/##[TYPE=ZombieHHChannel]')])
        )
    _logger.info("Total channels: %s" % nchans)
    return _records

def setupStimuls(compt):
    command = moose.PulseGen('%s/command' % compt.path)
    command.level[0] = 1e-9
    command.delay[0] = 0
    command.width[0] = 0.1
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

def countSpike():
    import count_spike
    global db_query_
    soma = None 
    for k in _records.keys():
        if "soma" in k.lower():
            soma = _records[k].vector 
            break
    if len(soma) > 0:
        nSpikes, meanDT, varDT = count_spike.spikes_characterization( soma )
        db_query_['number_of_spikes'] = nSpikes
        db_query_['mean_spike_interval'] = meanDT
        db_query_['variance_spike_interval'] = varDT
        _logger.info("[MOOSE] Spike characteristics:")
        _logger.info("\t num_spikes: {}, mean_dt: {}, var_dt: {}".format(
            nSpikes, meanDT, varDT)
            )

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
    db_query_['simulator'] = 'moose'
    db_query_['number_of_compartments'] = ncompts
    db_query_['number_of_channels'] = nchans
    db_query_['simulation_time'] = args.sim_time
    db_query_['run_time'] = t
    db_query_['dt'] = args.sim_dt
    db_query_['model_name'] = args.swc_file
    countSpike()
    dbEntry(db_query_)
    saveData(outfile="_data/moose.csv")

