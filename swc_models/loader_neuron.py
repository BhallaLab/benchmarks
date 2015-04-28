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

from neuron import h, gui
from collections import Counter, defaultdict
import sys
import re
import numpy as np
import pylab
import networkx as nx

topology = nx.DiGraph()

def instantiate_swc(filename):
    """load an swc file and instantiate it"""
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
    r =  np.sqrt(np.mean(
        np.array([xpoints.mean(), ypoints.mean(), zpoints.mean()])**2)
        )
    return r

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


def insertChannels(segments, exprs):
    """Insert channels in segments given by expr"""
    assert type(segments) == dict
    assert type(exprs) == defaultdict
    #segmentCluster = cluster(segments)

def addNode(sec):
    """Add a node to topolgoy"""
    global topolgoy
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

    topology.add_node(sec
            , label= label
            , segs = sec.allseg()
            , type=sec.hname()
            , shape = nodeType
            , length = sec.L
            , color = color
            , r = 0.0
            )

##
# @brief This fuction should be called from ./swc_loader.py file.
#
# @param filename
# @param args Command line arguments.
#
# @return None
def loadModel(filename, args=None):
    print("[INFO] Loading %s into NEURON" % filename)
    cell = instantiate_swc(filename)

    for sec in cell.allsec():
        addNode(sec)
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
    for e in nx.bfs_edges(topology, sourceNode):
        src, tgt = e
        topology.node[tgt]['r'] = topology.node[src]['r'] + src.L

    nx.draw(topology)
    nx.write_dot(topology, 'topology.dot')

    #channelExprDict = defaultdict(list)
    #if args.insert_channels:
        #for p in args.insert_channels:
            #channelName, segPat, expr = p.split(',')
            #for seg in segPat.split(":"):
                #channelExprDict[seg].append((channelName, expr))

    #insertChannels(segDict, channelExprDict)

if __name__ == '__main__':
    def main(filename):
        loadModel(filename, args)
    filename = sys.argv[1]
    loadModel(filename)
