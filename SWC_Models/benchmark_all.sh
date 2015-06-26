#!/usr/bin/env bash
# SEARCH SWC FILE AND GENERATE BENCHMARK
set -e

echo "Recompiling NEURON mechanism libraries"
nrnivmodl

if [ ! -d ./_data ]; then 
    mkdir -p _data
fi

SWCFILES=`find . -type f -name "*.swc"`
for file in $SWCFILES; do
    ./test_moose.sh $file
    ./test_nrn.sh $file
done
echo "All done"

