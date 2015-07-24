"""compare.py: 

    Pass two csv file, first moose and second neuron.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import csv
import numpy as np

data_ = {}

def get_index(query, row):
    for i, r in enumerate(row):
        if query.lower() in r.lower():
            return i

def get_vector(index, data):
    res = []
    for row in data:
        row = row.split(",")
        if row:
            res.append(row[index])
    return res


def compare(mooseCsv, nrnCsv):
    mooseData = None
    nrnData = None
    with open(mooseCsv, "r") as f:
        mooseTxt = f.read().split("\n")
        mooseHeader, mooseData = mooseTxt[0], mooseTxt[1:]
    with open(nrnCsv, "r") as f:
        nrnTxt = f.read().split("\n")
        nrnHeader, nrnData = nrnTxt[0], nrnTxt[1:]

    mooseList = mooseHeader.split(",")
    for i, row in enumerate(nrnHeader.split(",")):
        comptID = row.replace("table_", "")
        mooseId = get_index(comptID, mooseList)
        mooseVec = get_vector(mooseId, mooseData)
        nrnVec = get_vector(i, nrnData)
        data_[comptID] = (mooseVec, nrnVec)

    for k in data_:
        mooseVec, nrnVec = data_[k]
        print len(mooseVec), len(nrnVec)

def main():
    mooseFile = sys.argv[1]
    nrnrFile = sys.argv[2]
    compare(mooseFile, nrnrFile)


if __name__ == '__main__':
    main()
