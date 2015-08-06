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
import lxml.etree as ET
import datetime

dataFile_ = 'comparision_data.xml'
dataXml_ = ET.Element("comparision_data")
dataXml_.attrib['date'] =  datetime.datetime.now().isoformat()
dataXml_.attrib['format'] = 'numpy.ndarray'

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
    dataXml_ = ET.parse(dataFile_).getroot()
    for elem in dataXml_:
        comptName = elem.attrib['neuron']
        t, moose, nrn = elem[0], elem[1], elem[2]
        tVec = np.fromstring(t.text, sep=",")
        mooseVec = np.fromstring(moose.text, sep=",")
        nrnVec = np.fromstring(nrn.text, sep=",")
        ax0 = pylab.subplot(3, 1, 1)
        pylab.plot(tVec, mooseVec, label='moose')
        pylab.plot(tVec, nrnVec, label='nrn')
        ax1 = pylab.subplot(3, 1, 2)
        pylab.plot(tVec, mooseVec - nrnVec)
        ax2 = pylab.subplot(3, 1, 3)
        pylab.plot(tVec[1:], np.diff(mooseVec) - np.diff(nrnVec))
    ax1.set_title("MOOSE - NEURON")
    ax2.set_title("diff(MOOSE) - diff(NEURON)")
    pylab.legend(loc='best', framealpha=0.4)
    outfile = "./comparision_moose_nrn.png"
    print("Plotting diff results to : %s" % outfile)
    pylab.savefig(outfile)

def compare(mooseCsv, nrnCsv):
    writeDataToXml(mooseCsv, nrnCsv)
    plot()

def writeDataToXml(mooseCsv, nrnCsv):
    global dataXml_
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
    for i, comptName in enumerate(nrnHeader[1:]):
        nrnComptName = comptName.replace("table_", "")
        mooseComptId, mooseComptName = get_index(nrnComptName, mooseHeader[1:])
        print("%s %s- moose equivalent %s %s" % (i, nrnComptName, mooseComptId
            , mooseComptName))
        nrnVec = nrnData[i]
        mooseArray = np.zeros(len(nrnVec))
        for i, (t, v) in enumerate(zip(nrnTimeVec,nrnVec)):
            mooseVal = get_moose_val(t, mooseTimeVec, mooseData[mooseComptId])
            mooseArray[i] = mooseVal
        elem = ET.SubElement(dataXml_
                , "compartment"
                , attrib = { "moose" : str(mooseComptName), "neuron" : nrnComptName }
                )
        timeXml = ET.SubElement(elem
                , "time", attrib = { "name" : "time", "unit" : "second" } )
        timeXml.text = to_csv_string(nrnTimeVec)
        mooseXml = ET.SubElement(elem, "moose", attrib = { "unit" : "volt" })
        mooseXml.text = to_csv_string(mooseArray)
        nrnXml = ET.SubElement(elem, "nrn", attrib = { "unit" : "volt" })
        nrnXml.text = to_csv_string(nrnVec)

    with open(dataFile_, "w") as f:
        f.write(ET.tostring(dataXml_, pretty_print=True))
    print("Done writing data to %s" % dataFile_)

def main():
    mooseFile = sys.argv[1]
    nrnrFile = sys.argv[2]
    compare(mooseFile, nrnrFile)

if __name__ == '__main__':
    main()
