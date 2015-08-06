"""

    Pass two csv file, first moose and second neuron.

    The first column in each file is time vector which is our reference column
    for further processing.

    This script assumes that columns of both files have been sorted in a way
    that each column in one file has its equivalent in second file at the same
    index.


    For automatic comparision see ./compare.py file.

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
import datetime

def to_csv_string(array):
    return ','.join(['%.8f' % num for num in array])

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

def plot():
    pass

def compare(mooseCsv, nrnCsv):
    rewrite_data(mooseCsv, nrnCsv)
    plot()

def reformat(dataA, dataB, scaleB, offsetB = 0.0):
    """Reformat matrix with given scaling function.

    y = scaleB * x + offsetB

    """
    # Before we can stack these data together, we need to scale one of the data
    # matrix. 

    swapped = False
    if dataA.shape > dataB.shape:
        print("[DEBUG] Swapping matrix since A.shape > B.shape")
        swapped = True
        dataX, dataY = dataB, np.vectorize(lambda y : (y-offsetB)/scaleB)(dataA)
    else:
        dataX, dataY = dataA, np.vectorize(lambda y : y*scaleB+offsetB)(dataB)

    # First column in both X and Y are x-axis of plot. They should match for
    # doing any comparision. In following loop, we use linear interpolation to
    # recompute Y at each value of xxVec.
    xVec = dataX.T[0]
    x_yVec = dataY.T[0]

    newData = np.ndarray(shape=dataX.shape)
    newData[:,0] = xVec
    for i, colY in enumerate(dataY.T[1:]):
        # For each column of Y, recompute the values of y at x given in
        # referenceVec (which is the first column of dataX).
        newY = np.vectorize(lambda x : np.interp(x, x_yVec, colY))(xVec)
        newData[:,i+1] = newY


    if swapped:
        return newData, dataX
    else:
        return dataX, newData


def rewrite_data(mooseCsv, nrnCsv):
    global dataXml_
    mooseData = None
    nrnData = None
    with open(mooseCsv, "r") as f:
        mooseTxt = f.read().split("\n")
        mooseHeader, mooseData = mooseTxt[0].split(","), np.genfromtxt(mooseTxt[1:],
                delimiter=',')
    with open(nrnCsv, "r") as f:
        nrnTxt = f.read().split("\n")
        nrnHeader, nrnData = nrnTxt[0].split(','), np.genfromtxt(nrnTxt[1:],
                delimiter=',')

    try:
        nrnData, mooseData = reformat(nrnData, mooseData, scaleB = 1e3)
    except Exception as e:
        print("[WARNING] The function you use is very senesitive to data format"
                "Check the input format or fix the code."
                "It worked at the last commit with default input file"
                " mentioned in Makefile. "
                )
        raise e

    # write new data to csv file.
    mooseOutFile = "%s_out.csv" % mooseCsv
    with open(mooseOutFile, "w") as mooseF:
        print("[INFO] Writing to %s" % mooseOutFile)
        np.savetxt(mooseOutFile, mooseData, header=",".join(mooseHeader), delimiter=',')
    nrnOutfile = "%s_out.csv" % nrnCsv
    with open(nrnOutfile, "w") as nrnF:
        print("[INFO] Writing to %s" % nrnOutfile)
        np.savetxt(nrnOutfile, nrnData, header=",".join(nrnHeader),
                delimiter=",")
    print("... Done")

def main():
    mooseFile = sys.argv[1]
    nrnrFile = sys.argv[2]
    compare(mooseFile, nrnrFile)

if __name__ == '__main__':
    main()
