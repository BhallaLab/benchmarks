#!/usr/bin/env bash
set -e
export PYTHONPATH=/opt/moose3.0.1/python

SWCFILES=`find . -type f -name "*.swc"`
for file in $SWCFILES; do
    echo "Executing model $file"
    $PYC ./swc_loader.py -f $file -s neuron -t 1 -o nrn.png \
        -c "hd, *dend*:*apic*, 5e-2*(1+(r*3e4))" \
        -c "kdr, *, 100" \
        -c "na3, *soma:*dend*:*apic*, 250" \
        -c "nax, *axon, 1250" \
        -c "kap, *axon:*soma*, 300" \
        -c "kap, *dend:*apic*, 150*(1+sign(100-r*1e6)) * (1+(r*1e4))" \
        -c "kad, *dend:*apic*, 150*(1+sign(r*1e6-100))*(1+r*1e4)"
    break
done
echo "All done"

