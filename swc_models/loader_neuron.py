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

def instantiate_swc(filename):
    """load an swc file and instantiate it"""
    h.load_file('import3d.hoc')
    cell = h.Import3d_SWC_read()
    cell.input(filename)
    i3d = h.Import3d_GUI(cell, 0)
    i3d.instantiate(None)
    return i3d

def computeR(seg):
    """Compute the distance from soma
    Assuming soma is at (0,0,0)
    """
    xpoints = ypoints = zpoints = np.zeros(h.n3d(seg))
    for i in range(len(xpoints)):
        xpoints[i] = h.x3d(i, seg)
        ypoints[i] = h.y3d(i, seg)
        zpoints[i] = h.z3d(i, seg)
    r =  np.sqrt(np.mean(
        np.array([xpoints.mean(), ypoints.mean(), zpoints.mean()])**2)
        )
    return r

def insertChannels(segments, exprs):
    """Insert channels in segments given by expr"""
    assert type(segments) == dict
    assert type(exprs) == defaultdict


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

    segDict = {}
    for sec in cell.allsec():
        for i in sec.allseg(): segDict[sec.hname()] = i

    channelExprDict = defaultdict(list)
    if args.insert_channels:
        for p in args.insert_channels:
            channelName, segPat, expr = p.split(',')
            for seg in segPat.split(":"):
                channelExprDict[seg].append((channelName, expr))

    insertChannels(segDict, channelExprDict)

if __name__ == '__main__':
    def main(filename):
        loadModel(filename, args)
    filename = sys.argv[1]
    loadModel(filename)
