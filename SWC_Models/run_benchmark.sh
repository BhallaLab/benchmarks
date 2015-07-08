#!/usr/bin/env bash
# SEARCH SWC FILE AND GENERATE BENCHMARK
export PYTHONPATH=/opt/moose/python
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
    ./test_moose.sh "$file" || echo "+ [WARN] Could not run MOOSE on file $file"
    ./test_nrn.sh "$file" || echo "+ [WARN] Could not run NEURON on file $file"
    i=$((i+1))
    if [[ $i = $TOTAL ]]; then
        echo "... Done $TOTAL comparisions. Quitting"
        exit
    fi
done
notify-send "Benchmarking is done for $TOTAL files"

