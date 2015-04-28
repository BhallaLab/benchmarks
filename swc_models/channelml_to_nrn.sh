#!/bin/bash
if [ $# -lt 1 ]; then
    echo "USAGE: $0 filename"
    exit
fi
filename="$1"
echo "Converting $filename to NEURON"
python ./ConvertCML.py $filename
echo "Compiling ${filename/%xml/mod}"
nrnivmodl ${filename/%xml/mod}
