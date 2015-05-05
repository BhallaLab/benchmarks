#!/usr/bin/env python

"""swc_loader_neuron.py:

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
import pylab
import networkx as nx
import time
import moose.utils as mu
from _profile import *

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
    global nchan
    assert type(exprs) == defaultdict
    for k in exprs:
        expr = k.replace('*', '.*')
        typePat = re.compile(r'%s'%expr)
        for exp in exprs[k]:
            insert(typePat, exp)

def insert(pat, chan):
    """Insert the pattern into segments """
    global nchan
    chanName, expr = chan
    for sec in topology.nodes():
        secName = sec.hname()
        if pat.match(secName):
            expr = expr.replace('r', str(topology.node[sec]['r']))
            g = eval(expr)
            #print("|- Inserting {} into {} with conductance: {} uS".format(
                #chanName, secName, g)
                #)
            chan = sec.insert(chanName)
            h('gmax=%s' % (g))
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
        _records['t'].record(h._ref_t)

##
# @brief This fuction should be called from ./swc_loader.py file.
#
# @param filename
# @param args Command line arguments.
#
# @return None
def loadModel(filename, args=None):
    """Load model given in filename """


    print("[INFO] Loading %s into NEURON" % filename)
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

    # Do a BFS and compute the length of edges.
    # Get the source node. This node has no parents and it should be only 1.
    sourceNode = None
    for n in topology.nodes():
        if topology.in_degree(n) == 0:
            sourceNode = n
            break
    setupStimulus(sourceNode)
    for e in nx.bfs_edges(topology, sourceNode):
        src, tgt = e
        topology.node[tgt]['r'] = topology.node[src]['r'] + src.L

    channelExprDict = defaultdict(list)
    if args.insert_channels:
        for p in args.insert_channels:
            channelName, secPat, expr = p.split(',')
            for sec in secPat.split(":"):
                channelExprDict[sec].append((channelName, expr))
        insertChannels(channelExprDict)
    return None

def makePlots():
    global _args
    for k in _records:
        if 't' != k:
            pylab.plot(_records['t'], _records[k])
    if not _args.plots:
        pylab.show()
    else:
        print("[INFO] Saving neuron data to %s" % _args.plots)
        pylab.savefig(_args.plots)

def setupStimulus(sec):
    """Setup the stimulus"""
    global _args
    stim = h.IClamp(0.5, sec=sec)
    stim.amp = 10.0
    stim.delay = 5.0
    stim.dur = _args.sim_time

def main(args):
    global nseg, nchan, simulator, _args
    _args = args
    loadModel(args.swc_file, args)

    print("Done loading")
    h.init()
    print("[INFO] Running NEURON for %s sec" % args.sim_time)
    t1 = time.time()
    h.tstop = 1e3 * float(args.sim_time)
    h.run()
    t = time.time() - t1
    dbEntry(simulator=simulator
            , dt=1e-3*dt
            , no_of_compartments=nseg
            , no_of_channels=nchan
            , simtime=args.sim_time
            , runtime=t
            , model_name = args.swc_file
            )
    print("Time taken by neuron: %s sec" % t)
    makePlots()
