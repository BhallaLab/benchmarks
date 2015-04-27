#!/usr/bin/env bash
# -c : Insert channels, True/False
# -o : If given, plot to filename.
SWCFILES=`find . -type f -name "*.swc"`
if [ ! -f ./benchmark.csv ]; then
    echo "num_segments,tot_time,filepath" | tee benchmark.csv
fi
for file in $SWCFILES; do
    echo "Running model $file"
    output=`python ./swc_loader.py -f $file -s neuron -t 1.0 -o moose.png -c True`
    #numsegs=`expr match "$output" ".*NumSegs = \([0-9]\+\)"`
    #totTime=`expr match "$output" ".*tot time = \([0-9.]\+\)"`
    #echo $numsegs,$totTime,$file | tee -a benchmark.csv
    exit
done
echo "All done"
