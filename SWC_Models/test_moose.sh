#!/usr/bin/env bash
# This script test MOOSE on SWC model file.

export PYTHONPATH=/opt/moose/python
#SWCFILES=`find . -type f -name "*.swc"`

if [ $# -lt 1 ]; then
    echo "USAGE: $0 swc_file [plot]"
    exit;
fi

MODELFILE="$1"
PLOT="$2"

function runMOOSE 
{
    echo "Executing model $1"
    $PYC ./swc_loader.py -f $1 -s moose -t 1 \
        -i 0.0000000017 \
        -c "hd; *dend*,*apic*; Gbar; 5e-2*(1+(r*3e4))" \
        -c "kdr; *; Gbar; 100" \
        -c "na3; *soma,*dend*,*apic*; Gbar; 250" \
        -c "nax; *axon; Gbar; 1250" \
        -c "kap; *axon,*soma*; Gbar; 300" \
        -c "kap; *dend,*apic*; Gbar; 150*(1+sign(100-r*1e6)) * (1+(r*1e4))" \
        -c "kad; *dend,*apic*; Gbar; 150*(1+sign(r*1e6-100))*(1+r*1e4)"
}

function runAll 
{
    for file in $SWCFILES; do
        runMOOSE $file
    done
}

runMOOSE $MODELFILE $PLOT
