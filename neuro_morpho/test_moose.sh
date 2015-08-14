#!/usr/bin/env bash
# This script test MOOSE on SWC model file.

export PYTHONPATH=/opt/moose/python
#SWCFILES=`find . -type f -name "*.swc"`

PYC="gdb -ex r --args python"
PYC="python"

if [[ $# -lt 1 ]]; then
    echo "USAGE: $0 swc_file [plot]"
    exit;
fi

MODELFILE="$1"
PLOT="$2"

function runMOOSE 
{
    echo "Executing model $1"
    $PYC ./swc_loader.py -f $1 -s moose -t 10.0 \
        -i 0.0000000008 \
        -c "hd;#dend#,#apical#;Gbar;5e-2*(1+(p*3e4))" \
        -c "kdr;#;Gbar;100" \
        -c "na3;#soma#,#dend#,#apical#;Gbar;250" \
        -c "nax;#axon#;Gbar;1250" \
        -c "kap;#axon#,#soma#;Gbar;300" \
        -c "kap;#dend#,#apical#;Gbar;150*(1+sign(100-p*1e6)) * (1+(p*1e4))" \
        -c "kad;#dend#,#apical#;Gbar;150*(1+sign(p*1e6-100))*(1+p*1e4)"
}

function runAll 
{
    for file in $SWCFILES; do
        runMOOSE $file
    done
}

runMOOSE $MODELFILE $PLOT
