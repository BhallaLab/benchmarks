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
import sys


def instantiate_swc(filename):
    """load an swc file and instantiate it"""
    
    # load the NEURON library (just in case h is defined otherwise elsewhere)
    
    # a helper library, included with NEURON
    h.load_file('import3d.hoc')
    
    # load the data. Use Import3d_SWC_read for swc, Import3d_Neurolucida3 for
    # Neurolucida V3, Import3d_MorphML for MorphML (level 1 of NeuroML), or
    # Import3d_Eutectic_read for Eutectic. (There is also an 
    # Import3d_Neurolucida_read for old Neurolucida files, but I've never seen one
    # in practice; try Import3d_Neurolucida3 first.)
    cell = h.Import3d_SWC_read()
    cell.input(filename)

    # easiest to instantiate by passing the loaded morphology to the Import3d_GUI
    # tool; with a second argument of 0, it won't display the GUI, but it will allow
    # use of the GUI's features
    i3d = h.Import3d_GUI(cell, 0)
    i3d.instantiate(None)

def main(filename):
    instantiate_swc(filename)

if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)
