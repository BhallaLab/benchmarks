#!/usr/bin/env bash
SWCFILES=`find . -type f -name "*.swc"`
if [ ! -f ./benchmark.csv ]; then
    echo "num_segments,tot_time,filepath" | tee benchmark.csv
fi
for file in $SWCFILES; do
    echo "Running model $file"
    output=`python ./timeCA1Pyr.py $file`
    numsegs=`expr match "$output" ".*NumSegs = \([0-9]\+\)"`
    totTime=`expr match "$output" ".*tot time = \([0-9.]\+\)"`
    echo $numsegs,$totTime,$file | tee -a benchmark.csv
done
echo "All done"
