#!/bin/bash
set -e
set -x
rm -rf ./moose_results.csv ./nrn_out.dat
nrnivmodl chans
#export PYTHONPATH=/opt/moose/python
python ./check_equivalence.py ../../swc_models/wu/CNG_version/ko20x-07.CNG.swc
nrniv ./ko20x-07.CNG.swc.hoc
./xplot.py -i ./moose_results.csv -o moose_results.png -t "MOOSE"
./xplot.py -i ./nrn_out.dat -o ./nrnout.png -t "NEURON"
python compare.py moose_results.csv nrn_out.dat
