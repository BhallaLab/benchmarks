#!/usr/bin/env python
"""loader.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

def main(args):
    """Main function. """
    if args.simulator == 'moose':
        import loader_moose as l
    elif args.simulator == 'neuron':
        import loader_neuron as l
    model = l.loadModel(args.swc_file)

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Create the benchmarks.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--swc_file', '-f'
            , required = True
            , type = str
            , help = 'Model file in SWC format'
            )

    parser.add_argument('--simulator', '-s'
        , required = False
        , default = 'moose'
        , type = str
        , help = 'Ding dong'
        )

    parser.add_argument('--sim_time', '-t'
        , required = True
        , type = float
        , default = 1.0
        , help = 'Simulation time'
        )
    parser.add_argument('--save_data', '-s'
        , required = True
        , default = False
        , help = 'Save data?'
        )
    
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main(args)
