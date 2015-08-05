#!/usr/bin/env python

"""xplot.py: 

    This program uses matplotlib to plot xplot like data_.

Last modified: Wed Aug 05, 2015  06:23PM

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2013, NCBS Bangalore"
__credits__          = ["NCBS Bangalore", "Bhalla Lab"]
__license__          = "GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@iitb.ac.in"
__status__           = "Development"

import sys
import pylab
import numpy as np

data_ = {}
modifier_ = {}

def parseModifier(modFile):
    global modifier_
    print("[INFO] Parsing modifier file %s" % modFile)
    modText = modFile.read()
    for modline in modText.split("\n"):
        if not modline:
            continue
        lhs, rhs = modline.split('<-')
        output = lhs
        expr, input = rhs.split('$')
        modifier_[output.strip()] = (expr.strip(), input.strip())

def splitLine(line, delimiter=None):
    if not delimiter:
        return line.split()
    else:
        return line.split(delimiter)

def modifyData(filename, headers, data):
    global modifier_
    if not modifier_:
        return data
    for i, h in enumerate(headers):
        key = "%s#%s" % (filename, h)
        if key in modifier_:
            print "%s in modifier_" % key
            print data, data.shape
            print "col: %s" % i
            print data[:,i]

def buildData( file, args ):
    global data_ 
    with open(file, "r") as f:
        lines = f.read().split('\n')
    header = lines[0].split(',')
    d = np.genfromtxt(file, delimiter=',', skip_header=True)
    d = modifyData(file, header, d)
    data_[file] = d

def zipIt(ys):
    """ Zip an n-dims vector.
    There are as many sublists as there are elements in each element of list.
    """
    result = [[ ] for x in ys[0] ]
    for y in ys:
        for i, e in enumerate(y):
            result[i].append(e)
    return result

def plotData( args ):
    outFile = args.output
    global data_ 
    for file in data_:
        xvec, yx = data_[file]
        try:
            yvecs = zipIt(yx)
        except Exception as e:
            print("[FATAL] Failed to zip the given elements")
            sys.exit(0)
        for yvec in yvecs:
            pylab.plot(xvec, yvec)
    if args.title:
        pylab.title(str(args.title))
    if not outFile:
        pylab.show()
    else:
        print("[INFO] Saving plots to: {}".format( outFile ))
        pylab.savefig(outFile)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--file"
            , nargs = "+"
            , help = "xplot file to plot using matplotlib"
            )
    parser.add_argument("-o", "--output"
            , default = None
            , help = "Output file to store plot"
            )
    parser.add_argument("-t", "--title"
            , default = ""
            , help = "Title of the plot"
            )
    parser.add_argument('-m', '--modifier'
            , default = None
            , type = argparse.FileType('r')
            , help = "Preprocessing macros on data_. [Draft]"
            )
    args = parser.parse_args()
    if args.modifier:
        parseModifier(args.modifier)
    [ buildData(f, args) for f in args.file ]
    #plotData( args )
