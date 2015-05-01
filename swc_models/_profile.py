"""_profile.py: 

    This module is responsible for profiling data.

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

dataDir = '_data'
profileFile = 'profile.csv'

if not os.path.isdir(dataDir):
    os.makedirs(dataDir)

stamp = datetime.datetime.now().isoformat()

if os.path.exists(profileFile):
    os.rename(profileFile, os.path.join(dataDir, '%s_%s'%(profileFile, stamp)))

with open(profileFile, "w") as pF:
    pF.write("nseg,nchans,simtime,simulator,comment\n")

def insertLine(line):
    """Insert a line into profile file"""
    with open(profileFile, "a") as f:
        f.write("%s\n" % line)
