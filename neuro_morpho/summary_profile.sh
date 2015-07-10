#!/bin/bash
#set -x
set -e
# This script extracts quick number from database.

TABLENAME=${1:-table201507}
DB=`pwd`/_profile.sqlite
SQLITE="sqlite3 $DB"
echo "++ DB: $DB, Table: $TABLENAME"

# Total entries
moose_total=`$SQLITE "SELECT COUNT(*) FROM $TABLENAME WHERE simulator='moose'";`
nrn_total=`$SQLITE "SELECT COUNT(*) FROM $TABLENAME WHERE simulator='neuron'";`
echo "Total MOOSE entries: " $moose_total
echo "Total NEURON entries: " $nrn_total


# In this section, we compute the average number of channels and number of
# comparmtents in both MOOSE and NEURON.
avg_nrn_compt=`$SQLITE "SELECT AVG(number_of_compartments) FROM $TABLENAME WHERE
simulator='neuron'";`
avg_moose_compt=`$SQLITE "SELECT AVG(number_of_compartments) FROM $TABLENAME WHERE 
simulator='moose'";`
echo "Avg no of compartments in MOOSE: " $avg_moose_compt
echo "Avg no of compartments in NEURON: " $avg_nrn_compt

# NOTE: We assume that run time in each simulator is proportional to the number
# of compartments.
NRNFACTOR=`echo "$avg_moose_compt / $avg_nrn_compt" | bc -l`
echo "NRNFACTOR for compartment: $NRNFACTOR"

avg_moose_chan=`$SQLITE "SELECT AVG(number_of_channels) FROM $TABLENAME WHERE
    simulator='moose'";`
avg_nrn_chan=`$SQLITE "SELECT AVG(number_of_channels) FROM $TABLENAME WHERE
    simulator='neuron'";`
echo "Avg no of channels in MOOSE: " $avg_moose_chan
echo "Avg no of channels in NEURON: " $avg_nrn_chan
CHANNRNFACTOR=`echo "$avg_moose_chan / $avg_nrn_chan" | bc -l`
echo "NRNFACTOR for channel: $CHANNRNFACTOR"

# Get the moose entries
avg_nrn_runtime=`$SQLITE "SELECT AVG(run_time) FROM $TABLENAME WHERE simulator='neuron'";`
avg_moose_runtime=`$SQLITE "SELECT AVG(run_time) FROM $TABLENAME WHERE simulator='moose'";`

# On average, NEURON has 1/3.45 less no of compartment. Thereby average should
# be scaled by this number,
echo "Avg moose runtime: $avg_moose_runtime"
echo "Avg neuron runtime:" `echo "$NRNFACTOR * $avg_nrn_runtime" | bc`

# NEURON performance for smaller models n < 1000.
nrn_per_compt_run_time=`$SQLITE "SELECT AVG(run_time/number_of_compartments) FROM $TABLENAME \
    WHERE simulator='neuron' AND number_of_compartments < 1000";`
moose_per_compt_run_time=`$SQLITE "SELECT AVG(run_time/number_of_compartments) FROM $TABLENAME \
    WHERE simulator='moose' AND number_of_compartments < 1000";`

echo "Per compt. run time (nrn/moose) < 1000 compts"
printf "\t $nrn_per_compt_run_time / $moose_per_compt_run_time \n"

# NEURON performance for smaller models n > 3000
nrn_per_compt_run_time=`$SQLITE "SELECT AVG(run_time/number_of_compartments) FROM $TABLENAME \
    WHERE simulator='neuron' AND number_of_compartments > 3000";`
moose_per_compt_run_time=`$SQLITE "SELECT AVG(run_time/number_of_compartments) FROM $TABLENAME \
    WHERE simulator='moose' AND number_of_compartments > 3000";`

echo "Per compt. run time (nrn/moose) > 3000 compts"
printf "\t $nrn_per_compt_run_time / $moose_per_compt_run_time"

