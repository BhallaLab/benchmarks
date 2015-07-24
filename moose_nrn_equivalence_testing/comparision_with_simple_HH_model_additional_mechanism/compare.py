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
    assert np.allclose(nrnTimeVec, mooseTimeVec), mooseTimeVec - nrnTimeVec
    for i, comptName in enumerate(nrnHeader[1:]):
        if i == 1:
            break 
        nrnComptName = comptName.replace("table_", "")
        mooseComptId, mooseComptName = get_index(nrnComptName, mooseHeader[1:])
        print("%s %s- moose equivalent %s %s" % (i, nrnComptName, mooseComptId,
            mooseComptName))
        pylab.plot(nrnTimeVec, nrnData[i] - mooseData[mooseComptId],
                label="neuron-%s, moose-%s" % (comptName, mooseComptName))
    pylab.legend(loc='best', framealpha=0.4)
    pylab.show()


#   mooseList = mooseHeader.split(",")
    #for i, row in enumerate(nrnHeader.split(",")):
        #comptID = row.replace("table_", "")
        #mooseId = get_index(comptID, mooseList)
        #mooseVec = get_vector(mooseId, mooseData)
        #nrnVec = get_vector(i, nrnData)
        #data_[comptID] = (mooseVec, nrnVec)

    #for k in data_:
        #mooseVec, nrnVec = data_[k]
        #print len(mooseVec), len(nrnVec)

def main():
    mooseFile = sys.argv[1]
    nrnrFile = sys.argv[2]
    compare(mooseFile, nrnrFile)


if __name__ == '__main__':
    main()
