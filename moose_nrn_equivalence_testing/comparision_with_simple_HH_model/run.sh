#!/bin/bash
set -e
set -x
rm -rf ./moose_results.csv ./nrn_out.dat
nrnivmodl *.mod chans
#export PYTHONPATH=/opt/moose/python
MODELFILE=ko20x-07.CNG.swc
python ./check_equivalence.py $MODELFILE
nrniv $MODELFILE.hoc
./xplot.py -i ./moose_results.csv -o moose_results.png -t "MOOSE"
./xplot.py -i ./nrn_out.dat -o ./nrnout.png -t "NEURON"
python compare.py moose_results.csv nrn_out.dat
