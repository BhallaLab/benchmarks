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

def main():


if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Create the benchmarks.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--variable', '-v', metavar='variable'
            , required = True
            , help = 'A generic option'
            )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main()
