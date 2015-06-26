#!/usr/bin/env bash
# This script test MOOSE on SWC model file.

#SWCFILES=`find . -type f -name "*.swc"`
MODELFILE="$1"

if [ $# -lt 1 ]; then
    echo "USAGE: $0 swc_file"
    exit;
fi

function runMOOSE 
{
    echo "Executing model $1"
    $PYC ./swc_loader.py -f $1 -s moose -t 1 -o moose.eps \
        -i 0.000000001 \
        -c "hd; *dend*,*apic*; 5e-2*(1+(r*3e4))" \
        -c "kdr; *; 100" \
        -c "na3; *soma,*dend*,*apic*; 250" \
        -c "nax; *axon; 1250" \
        -c "kap; *axon,*soma*; 300" \
        -c "kap; *dend,*apic*; 150*(1+sign(100-r*1e6)) * (1+(r*1e4))" \
        -c "kad; *dend,*apic*; 150*(1+sign(r*1e6-100))*(1+r*1e4)"
}

function runAll 
{
    for file in $SWCFILES; do
        runMOOSE $file
    done
}

runMOOSE $MODELFILE
