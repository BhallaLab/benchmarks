# Compare moose and neuron data.
import sys
import numpy as np

def get_nrn_index(mooseHeader, nrnHeader):
    for i, v in enumerate(mooseHeader):

def compare(mooseFile, nrnFile):
    with open(mooseFile, "r") as f:
        mooseText = f.read().split('\n')
    with open(nrnFile, "r") as f:
        nrnText = f.read().split('\n')
    mooseHeader, nrnHeader= mooseText[0].split(','), nrnText[0].split(',')
    mooseData = np.genfromtxt(mooseText, skiprows=1, delimiter=',')
    nrnData = np.genfromtxt(nrnText, skiprows=1, delimiter=' ')
    nrnIndices = get_nrn_index( mooseHeader, nrnHeader )

def main():
    mooseFile = sys.argv[1]
    nrnFile = sys.argv[2]
    compare(mooseFile, nrnFile)

if __name__ == '__main__':
    main()
