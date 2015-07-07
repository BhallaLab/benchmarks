#!/usr/bin/env bash
# SEARCH SWC FILE AND GENERATE BENCHMARK
#set -e

TOTAL="$1"

echo "Recompiling NEURON mechanism libraries"
mkdir -p _log
nrnivmodl chans &> nrnivmodel.log 
mkdir -p _data

SWCFILES=`find -L ./SWCDATA -type f -name "*.swc"`
i=0
for file in $SWCFILES; do
    echo "||| Using modelfile $file"
    ( ./test_moose.sh "$file" && ./test_nrn.sh "$file" )
    i=$((i+1))
    if [[ $i = $TOTAL ]]; then
        echo "Done $TOTAL comparisions. Quitting"
        exit
    fi
done
echo "All done"

