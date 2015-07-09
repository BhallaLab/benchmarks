#!/usr/bin/env bash
# SEARCH SWC FILE AND GENERATE BENCHMARK
export PYTHONPATH=/opt/moose/python
#set -e
TOTAL="$1"

mkdir -p _data
mkdir -p _log

function runNRN
{
    echo "Recompiling NEURON mechanism libraries"
    nrnivmodl chans &> nrnivmodel.log 
    ./test_nrn.sh "$file" || echo "+ [WARN] Could not run NEURON on file $file"
}

function runMOOSE
{
    ./test_moose.sh "$1" || echo "+ [WARN] Could not run MOOSE on file $1"
}


SWCFILES=`find -L ../swc_models -type f -name "*.swc"`
declare -i i
i=0
for file in $SWCFILES; do
    #runNRN $file
    runMOOSE $file
    i=$((i+1))
    if [[ $i = $TOTAL ]]; then
        echo "... Done $TOTAL comparisions. Quitting"
        exit
    fi
done
notify-send "Benchmarking is done for $TOTAL files"
