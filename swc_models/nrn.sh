#!/usr/bin/env bash
# -c : Insert channels, True/False
# -o : If given, plot to filename.
SWCFILES=`find . -type f -name "*.swc"`
if [ ! -f ./benchmark.csv ]; then
    echo "num_segments,tot_time,filepath" | tee benchmark.csv
fi
for file in $SWCFILES; do
    echo "Executing model $file"
    (
    python ./swc_loader.py -f $file -s neuron -t 1.0 -o nrn.png \
        -c "hd, *dend*:*apical*, 5e-2*(1+(r*3e4))" \
        -c "kdr, *, 100" \
        -c "na3, *soma:*dend*:*apical*, 250" \
        -c "nax, *axon, 1250" \
        -c "kap, *axon:*soma*, 300" \
        -c "kap, *dend:*apical*, 150*(1+sign(100-r*1e6)) * (1+(r*1e4))" \
        -c "kad, *dend:*apical*, 150*(1+sign(r*1e6-100))*(1+r*1e4)"
    )
    break
done

echo "Turning topology to eps file"
fdp -Teps ./topology.dot > topology.eps
echo "All done"

