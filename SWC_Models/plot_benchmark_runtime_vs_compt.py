"""plot_benchmark_runtime_vs_compt.py: 

    Plot benchmark.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import os
import sys
import sqlite3 as sql 

dbpath = os.path.join('.', '_profile.sqlite')
db = sql.connect(dbpath)
curr = db.cursor()

def getMOOSE():
    query = """SELECT runtime, no_of_compartments FROM swc WHERE
    simulator='moose' ORDER BY no_of_compartments"""
    for row in curr.execute(query):
        print row

def getNRN():
    pass

def main():
    moose = getMOOSE()
    nrn = getNRN()


if __name__ == '__main__':
    main()
