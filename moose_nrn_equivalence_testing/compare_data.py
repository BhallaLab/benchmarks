# Compare moose and neuron data.
import sys
import numpy as np
import pylab

def get_nrn_index(mooseHeader, nrnHeader):
    for i, v in enumerate(mooseHeader):
        print i, v
    print nrnHeader

def compare(mooseFile, nrnFile):
    with open(mooseFile, "r") as f:
        mooseText = f.read().split('\n')
    with open(nrnFile, "r") as f:
        nrnText = f.read().split('\n')
    mooseHeader, nrnHeader= mooseText[0].split(','), nrnText[0].split(',')
    mooseData = np.genfromtxt(mooseText, skiprows=1, delimiter=',')
    # Make units similar.
    nrnData = 1e-3*np.genfromtxt(nrnText, skiprows=1, delimiter=',')
    nrnIndices = get_nrn_index( mooseHeader, nrnHeader )
    xvec = nrnData[:,0]
    for i, col in enumerate(nrnData[:,1:2].T):
        pylab.plot(xvec, col, label="%s" % i)
    #pylab.legend(loc='best', framealpha=0.4)

    mooseVec = mooseData[:,0]
    for i, col in enumerate(mooseData[:,1:2].T):
        pylab.plot(mooseVec, col, label = '%s' % i)

    pylab.show()

def main():
    mooseFile = sys.argv[1]
    nrnFile = sys.argv[2]
    compare(mooseFile, nrnFile)

if __name__ == '__main__':
    main()
