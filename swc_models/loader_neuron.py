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
import sys

def instantiate_swc(filename):
    """load an swc file and instantiate it"""
    h.load_file('import3d.hoc')
    cell = h.Import3d_SWC_read()
    cell.input(filename)
    i3d = h.Import3d_GUI(cell, 0)
    i3d.instantiate(None)
    return i3d

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
    print cell
    for sec in cell.allsec():
        print sec


if __name__ == '__main__':
    def main(filename):
        loadModel(filename, args)
    filename = sys.argv[1]
    loadModel(filename)
