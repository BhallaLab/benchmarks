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

BUILD_DIR=`pwd`/_build

mkdir -p $BUILD_DIR
(
    cd $BUILD_DIR
    cmake ..
    make -j2
    echo "[INFO] I am done compiling required binaries using cmake."
)

for i in {2,4,8,16,18}; do
    echo "[INFO] Running with $i threads"
    OPENMP_NUM_THREADS=$i $BUILD_DIR/benchmark_rng_openmp
done
echo "[INFO] Check the csv file in $BUILD_DIR. It has benchmarks"
