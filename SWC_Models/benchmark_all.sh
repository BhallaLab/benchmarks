#!/usr/bin/env bash
# SEARCH SWC FILE AND GENERATE BENCHMARK
set -e

echo "Recompiling NEURON mechanism libraries"
nrnivmodl

SWCFILES=`find . -type f -name "*.swc"`
for file in $SWCFILES; do
    ./test_moose.sh $file
    ./test_nrn.sh $file
    break
done
echo "All done"

