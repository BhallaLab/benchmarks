#!/bin/bash
set -e
rm -rf ./moose_results.csv ./nrn_out.dat
export PYTHONPATH=/opt/moose/python
./check_equivalence.py ../../swc_models/wu/CNG_version/ko20x-07.CNG.swc
nrnivmodl chans
nrniv ./ko20x-07.CNG.swc.hoc
./xplot.py -i ./moose_results.csv -o moose_results.png
./xplot.py -i ./nrn_out.dat -o ./nrnout.png
# just get soma value
echo "Plotting moose soma against nrn soma"

