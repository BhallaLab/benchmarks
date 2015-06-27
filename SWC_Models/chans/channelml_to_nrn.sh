#!/bin/bash
xmlfiles=`find . -name "*.xml"`
for filename in $xmlfiles; do
    echo "Converting $filename to NEURON"
    python ./ConvertCML.py $filename 
done
nrnivmodl
