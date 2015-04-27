#!/usr/bin/env bash
set -e
# -c : Insert channels, True/False
# -o : If given, plot to filename.
SWCFILES=`find . -type f -name "*.swc"`
if [ ! -f ./benchmark.csv ]; then
    echo "num_segments,tot_time,filepath" | tee benchmark.csv
fi
for file in $SWCFILES; do
    echo "Executing model $file"
    python ./swc_loader.py -f $file -s neuron -t 1.0 -o nrn.png
    exit
done
echo "All done"
