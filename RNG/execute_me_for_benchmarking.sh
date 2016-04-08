#!/bin/bash - 
#===============================================================================
#
#          FILE: execute_me_for_benchmarking.sh
# 
#         USAGE: ./execute_me_for_benchmarking.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Dilawar Singh (), dilawars@ncbs.res.in
#  ORGANIZATION: NCBS Bangalore
#       CREATED: 04/08/2016 12:37:15 PM
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
set -e

BUILD_DIR=`pwd`/_build

mkdir -p $BUILD_DIR
echo "Doing with GSL"
(
    echo "Compilation flags: $@"
    cd $BUILD_DIR
    cmake "$@" ..
    make -j2
    echo "[INFO] I am done compiling required binaries using cmake."
)
NOW=$(date +"%Y_%m_%d__%H_%M_%S")
mv ./benchmarkdata.csv ./_data/benchmarkdata_${NOW}.csv
for i in {1,2,3,4,5,6,7,8,16,24,32}; do
    echo "[INFO] Running with $i threads"
    OPENMP_NUM_THREADS=$i $BUILD_DIR/benchmark_rng_openmp
done
echo "[INFO] Check the csv file in $BUILD_DIR. It has benchmarks"
