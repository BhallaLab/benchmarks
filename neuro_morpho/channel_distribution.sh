#!/usr/bin/env bash
echo "This script dumps the channel per comparment for each simulator"
DBNAME=_profile.sqlite
TABLE=table201507
SQLITE="sqlite3  $DBNAME"

mooseChans=`$SQLITE "SELECT number_of_channels/number_of_compartments FROM
$TABLE where simulator='neuron';"`
echo $mooseChans
