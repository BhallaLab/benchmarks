#!/usr/bin/env bash
# SEARCH SWC FILE AND GENERATE BENCHMARK
export PYTHONPATH=/opt/moose/python
mkdir -p _data
mkdir -p _log

function runMOOSE
{
    ./test_moose.sh "$1" || echo "+ [WARN] Could not run MOOSE on file $1"
}

files=`find .. -name "*.swc" -type f`
for f in $files; do
    if grep -Fxq "$f" ./_done_moose.txt ; then
        echo "$f already done"
    else
        echo "need to do $f"
        runMOOSE $f
    fi
done
