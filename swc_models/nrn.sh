#!/usr/bin/env bash
__ScriptVersion="0.1"

#===  FUNCTION  ================================================================
#         NAME:  usage
#  DESCRIPTION:  Display usage information.
#===============================================================================
function usage ()
{
        cat <<- EOT

  Usage :  $0 [options] [--]

  Options:
  -h|help       Display this message
  -v|version    Display script version
  -x|debug      Run python in debug mode.

EOT
}    # ----------  end of function usage  ----------

#-----------------------------------------------------------------------
#  Handle command line arguments
#-----------------------------------------------------------------------

debug=0
while getopts ":hvx" opt
do
  case $opt in
    h|help     )  usage; exit 0   ;;
    v|version  )  echo "$0 -- Version $__ScriptVersion"; exit 0   ;;
    x|debug    )  debug=1 ;;
    \? )  echo -e "\n  Option does not exist : $OPTARG\n"
          usage; exit 1   ;;
  esac    # --- end of case ---
done
shift $(($OPTIND-1))

PYC=python
if [ $debug = 0 ]; then
    continue
else
    echo "Debugging mode"
    PYC="gdb -ex r --args $PYC"
fi

SWCFILES=`find . -type f -name "*.swc"`
if [ ! -f ./benchmark.csv ]; then
    echo "num_segments,tot_time,filepath" | tee benchmark.csv
fi
for file in $SWCFILES; do
    echo "Executing model $file"
    $PYC ./swc_loader.py -f $file -s neuron -t 1.0 -o nrn.png \
        -c "hd, *dend*:*apic*, 5e-2*(1+(r*3e4))" \
        -c "kdr, *, 100" \
        -c "na3, *soma:*dend*:*apic*, 250" \
        -c "nax, *axon, 1250" \
        -c "kap, *axon:*soma*, 300" \
        -c "kap, *dend:*apic*, 150*(1+sign(100-r*1e6)) * (1+(r*1e4))" \
        -c "kad, *dend:*apic*, 150*(1+sign(r*1e6-100))*(1+r*1e4)"
    break
done

echo "Turning topology to eps file"
topFile=./topology.dot
if [ -f $topFile ]; then
    fdp -Teps $topFile > $topFile.eps
else
    echo "No $topFile generated"
fi
echo "All done"

