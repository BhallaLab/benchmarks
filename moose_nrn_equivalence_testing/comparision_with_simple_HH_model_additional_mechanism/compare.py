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
import pylab

data_ = {}

def get_index(query, row):
    for i, r in enumerate(row):
        r = r.split("/")[-1]
        if query.lower()+"[0]" == r.lower():
            return i, r
    raise Exception

def zip_with_time(timevec, datavecs):
    data = []
    for d in datavecs:
        data.append(zip(timevec, d))
    return data

def get_moose_val(t, mooseTimeVec, mooseVec):
    return np.interp(t, mooseTimeVec, mooseVec)
    
def compare(mooseCsv, nrnCsv):
    mooseData = None
    nrnData = None
    with open(mooseCsv, "r") as f:
        mooseTxt = f.read().split("\n")
        mooseHeader, mooseData = mooseTxt[0].split(","), np.genfromtxt(mooseTxt[1:],
                delimiter=',').T
    with open(nrnCsv, "r") as f:
        nrnTxt = f.read().split("\n")
        nrnHeader, nrnData = nrnTxt[0].split(','), 1e-3*np.genfromtxt(nrnTxt[1:],
                delimiter=',').T

    nrnTimeVec, nrnData = nrnData[0], nrnData[1:]
    mooseTimeVec, mooseData = mooseData[0], mooseData[1:]
    outFile = open("comparision_data.xml", "w")
    for i, comptName in enumerate(nrnHeader[1:]):
        nrnComptName = comptName.replace("table_", "")
        mooseComptId, mooseComptName = get_index(nrnComptName, mooseHeader[1:])
        outFile.write('<{0} format="csv" moose_id="{1}" nrn_id="{2}
                header="time,moose,neuron"">\n'.format(
            nrnComptName, mooseComptName, nrnComptName))
        print("%s %s- moose equivalent %s %s" % (i, nrnComptName, mooseComptId
            , mooseComptName))
        nrnvec = nrnData[i]
        moosevec = []
        xvec = []
        for i, (t, v) in enumerate(zip(nrnTimeVec,nrnvec)):
            mooseVal = get_moose_val(t, mooseTimeVec, mooseData[mooseComptId])
            outFile.write("{0},

    outFile.close()

def main():
    mooseFile = sys.argv[1]
    nrnrFile = sys.argv[2]
    compare(mooseFile, nrnrFile)


if __name__ == '__main__':
    main()
