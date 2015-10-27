#!/bin/bash
nrnivmodl chans
MODELFILE=ko20x-01.CNG.swc
FILENAME=`basename $MODELFILE`
HOCFILE=$FILENAME.hoc

echo $HOCFILE
python ./check_equivalence.py $MODELFILE

echo "Running generated $HOCFILE"
nrniv $HOCFILE

echo "You should have nrn_out.dat and moose_out.csv files in the current 
working directory. 

NOTICE: While neuron saves Vm from all compartment, we have configured MOOSE to
store Vm from few compartments. You have to search in nrn_out.dat file for
equivalent section. Also MOOSE uses SI units while NEURON uses milli-seconds and
milli-volts."
