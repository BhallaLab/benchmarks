"""loader_neuron.py:

    Load an SWC file in neuron.

"""
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

from neuron import h
from collections import Counter, defaultdict
import sys
import re
import numpy as np
import csv
import pylab
import networkx as nx
import time
from _profile import *
query_dict_ = {}

import logging
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='nrn.log',
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

topology = nx.DiGraph()
sign = np.sign

h.dt = 5e-3
nseg = 0
nchan = 0
dt = h.dt
simulator = 'neuron'
_args = None
_records = { 't' : h.Vector() }

def instantiate_swc(filename):
    """load an swc file and instantiate it"""
    h.load_file('stdgui.hoc')
    h.load_file('import3d.hoc')
    cell = h.Import3d_SWC_read()
    cell.input(filename)
    i3d = h.Import3d_GUI(cell, 0)
    i3d.instantiate(None)
    return i3d

def computeCenter(seg):
    """Compute the distance from soma
    Assuming soma is at (0,0,0)
    """

    # n3d returns the number of 3d points in a segment. 
    xpoints = ypoints = zpoints = np.zeros(h.n3d(seg))
    for i in range(len(xpoints)):
        xpoints[i] = h.x3d(i, seg)
        ypoints[i] = h.y3d(i, seg)
        zpoints[i] = h.z3d(i, seg)
    center = np.array([xpoints.mean(), ypoints.mean(), zpoints.mean()])
    r =  np.sqrt(np.mean(center))
    return r, center

def computeSectionLength(sec):
    return sec.L


def cluster(segDict):
    pat = re.compile(r'(?P<name>\w+)\[(?P<index>\d+)\]')
    sortedKeys = sorted(segDict)
    sortedDict = {}
    for k in sortedKeys:
        sortedDict[k] = segDict[k]
        
    clusterDict = defaultdict(list)
    for k in sortedDict:
        m = pat.match(k)
        name, index = m.group('name'), m.group('index')
        clusterDict[name].append(sortedDict[k])


def insertChannels(exprs):
    """Insert channels in segments given by expr"""
    assert type(exprs) == defaultdict
    for k in exprs:
        expr = k.replace('#', '.*')
        typePat = re.compile(r'%s'%expr)
        for exp in exprs[k]:
            insert(typePat, exp)
    _logger.debug("Total channels in neuron: %s" % nchan)

def insert(pat, chan):
    """Insert the pattern into segments """
    global nchan
    chanName, expr = chan
    for sec in topology.nodes():
        secName = sec.hname()
        if pat.match(secName):
            expr = expr.replace('p', str(topology.node[sec]['r']))
            g = eval(expr)
            _logger.debug("|- Inserting {} into {} with conductance: {} uS".format( chanName, secName, g))
            for i in range(2):
                try:
                    sec.insert(chanName)
                except Exception as e:
                    #_logger.debug("[INFO] Using HOC statement to insert")
                    h('{0} insert {1}'.format(secName, chanName))
                    h('\tg_{}={}'.format(chanName,g))
                nchan += 1

# NOTE: Calling this function causes segmentation fault.
def centerOfSec(sec):
    centers = []
    for seg in sec.allseg():
        centers.append(computeCenter(seg))

def addNode(sec, record=False):
    """Add a node to topolgoy

    if `record=True` then also add a recorder to plot.
    """
    global topolgoy, _records, nseg
    label = sec.hname()
    nodeType = 'box'
    if "soma" in label.lower():
        nodeType = 'circle'
        color = 'red'
    elif 'dend' in label.lower():
        color = 'blue'
    elif 'axon' in label.lower():
        color = 'yellow'
    else:
        color = 'blue'
    nseg += sec.nseg
    topology.add_node(sec
            , label= label
            , segs = sec.allseg()
            , type=sec.hname()
            , shape = nodeType
            , length = sec.L
            , color = color
            , r = 0.0
            )
    if record:
        _records[label] = h.Vector()
        _records[label].record(sec(0.5)._ref_v)

##
# @brief This fuction should be called from ./swc_loader.py file.
#
# @param filename
# @param args Command line arguments.
#
# @return None
def loadModel(filename, args=None):
    """Load model given in filename """

    _logger.debug("Loading %s into NEURON" % filename)
    cell = instantiate_swc(filename)
    for sec in cell.allsec():
        addNode(sec, record=True)
        for child in sec.children():
            addNode(child)
            scaleLength = 50
            topology.add_edge(sec, child
                    , label='%.1f'%(child.L)
                    , len=child.L/scaleLength
                    , minlen=child.L/scaleLength
                    )
    _records['t'].record(h._ref_t)

    # Do a BFS and compute the length of edges.
    # Get the source node. This node has no parents and it should be only 1.
    sourceNode = None
    for n in topology.nodes():
        if topology.in_degree(n) == 0:
            sourceNode = n
            break
    _logger.debug("Found parent node %s" % sourceNode)
    for e in nx.bfs_edges(topology, sourceNode):
        src, tgt = e
        topology.node[tgt]['r'] = topology.node[src]['r'] + src.L

    channelExprDict = defaultdict(list)
    if args.insert_channels:
        for p in args.insert_channels:
            channelName, secPat, gbar, expr = p.split(';')
            for sec in secPat.split(","):
                sec = sec.strip()
                channelExprDict[sec].append((channelName, expr))

        insertChannels(channelExprDict)

    # Add a stimulus to sourceNode.
    addStim(sourceNode)
    return None

def saveData(outfile):
    """Save data to a csv file"""
    xvec = _records['t']
    yvec = _records['soma[0]']
    with open(outfile, 'wb') as f:
        fnames = [ 't', 'soma' ]
        f.write(",".join(fnames)+"\n")
        for i, x in enumerate(xvec):
            f.write("%s,%s\n" % (1e-3*x, 1e-3*yvec[i]))
    _logger.debug("Done writing data to %s" % outfile)

def countSpike( ):
    import count_spike
    soma = _records['soma[0]']
    numSpikes, meanDt, varDt = count_spike.spikes_characterization( soma )
    query_dict_['number_of_spikes'] = numSpikes
    query_dict_['mean_spike_interval'] = meanDt
    query_dict_['variance_spike_interval'] = varDt
    _logger.info("Neuron: #spike={}, mean={}, variance={}".format(
        numSpikes , meanDt , varDt)
        )

def makePlots():
    global _args
    #for k in _records:
        #if 't' != k:
            #pylab.plot(_records['t'], _records[k], label=k)
    pylab.figure(figsize=(10, 2.0))
    pylab.plot(_records['t'], _records['soma[0]'], label='Soma Vm')
    pylab.xlabel('Time (ms)')
    pylab.ylabel('Vm (mV)')
    pylab.title("Neuron")
    if not _args.plots:
        pylab.show()
    else:
        _logger.info("Saving neuron data to %s" % _args.plots)
        #pylab.show()
        pylab.savefig(_args.plots)

def addStim(section):
    """Setup the stimulus"""
    global _args
    _logger.debug("Adding a pulsegen (%s A) at %s" % (_args.inject,
        section.hname()))
    h('access %s' % section.hname())
    h('objectvar stim')
    h('stim = new IClamp(0.5)')
    h('stim.amp = %s' % (_args.inject*1e9))
    h('stim.dur = %s' % (1e3*_args.sim_time))

def main(args):
    global nseg, nchan, simulator, _args
    _args = args
    loadModel(args.swc_file, args)
    h('cvode_active(1)')
    h.init()
    t1 = time.time()
    h.tstop = 1e3 * float(args.sim_time)
    h.run()
    t = time.time() - t1
    countSpike()
    query_dict_['number_of_compartments'] = nseg
    query_dict_['number_of_channels'] = nchan
    query_dict_['simulator'] = 'neuron'
    query_dict_['dt'] = 1e-3*dt
    query_dict_['model_name'] = args.swc_file
    query_dict_['run_time'] = t
    query_dict_['simulation_time'] = 1e3*args.sim_time
    dbEntry( query_dict_ )
    saveData('_data/nrn.csv')

