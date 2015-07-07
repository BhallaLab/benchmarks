#!/bin/bash
#set -x
set -e
# This script extracts quick number from database.

DB=`pwd`/_profile.sqlite
SQLITE="sqlite3 $DB"

# In this section, we compute the average number of channels and number of
# comparmtents in both MOOSE and NEURON.
avg_nrn_compt=`$SQLITE "SELECT AVG(no_of_compartments) FROM swc WHERE
simulator='neuron'";`
avg_moose_compt=`$SQLITE "SELECT AVG(no_of_compartments) FROM swc WHERE 
simulator='moose'";`
echo "Avg no of compartments in MOOSE: " $avg_moose_compt
echo "Avg no of compartments in NEURON: " $avg_nrn_compt

# NOTE: We assume that run time in each simulator is proportional to the number
# of compartments.
NRNFACTOR=`echo "$avg_moose_compt / $avg_nrn_compt" | bc -l`
echo "NRNFACTOR for compartment: $NRNFACTOR"

avg_moose_chan=`$SQLITE "SELECT AVG(no_of_channels) FROM swc WHERE
    simulator='moose'";`
avg_nrn_chan=`$SQLITE "SELECT AVG(no_of_channels) FROM swc WHERE
    simulator='neuron'";`
echo "Avg no of channels in MOOSE: " $avg_moose_chan
echo "Avg no of channels in NEURON: " $avg_nrn_chan
CHANNRNFACTOR=`echo "$avg_moose_chan / $avg_nrn_chan" | bc -l`
echo "NRNFACTOR for channel: $CHANNRNFACTOR"

# Get the moose entries
avg_nrn_runtime=`$SQLITE "SELECT AVG(runtime) FROM swc WHERE simulator='neuron'";`
avg_moose_runtime=`$SQLITE "SELECT AVG(runtime) FROM swc WHERE simulator='moose'";`

# On average, NEURON has 1/3.45 less no of compartment. Thereby average should
# be scaled by this number,
echo "Avg moose runtime: $avg_moose_runtime"
echo "Avg neuron runtime:" `echo "$NRNFACTOR * $avg_nrn_runtime" | bc`
