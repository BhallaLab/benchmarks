#!/usr/bin/env python

import os
import moose
import moose.utils as mu
import sys
import pylab
from collections import defaultdict
import moose_to_neuron as m2n

nrn_segs_ = {}
moose_compts_ = {}
soma_ = None
nrn_text_ = {} #defaultdict(list)
model_name_ = None
records_ = {}
dt_ = 50e-6

chanProto_ = [
        ['./cellMechanisms/KConductance/KChannel_HH.xml'], 
        ['./cellMechanisms/NaConductance/NaChannel_HH.xml'],
        ['./cellMechanisms/LeakConductance/LeakConductance.xml'],
        [ './chans/kdr.xml' ]
        ]

passiveDistrib_ = [ 
        [ ".", "#", "RM", "2.8", "CM", "0.01", "RA", "1.5",  
            "Em", "-58e-3", "initVm", "-65e-3" ]
        , [ ".", "#axon#", "RA", "0.5" ] 
        ]

chanDistrib_ = [
        [  "NaConductance", "#", "Gbar", "1200" ]
        , [ "KConductance", "#", "Gbar", "360" ]
        , [ "LeakConductance", "#", "Gbar", "3" ]
        , [ "kdr", "#", "Gbar", "10" ]
        ]

def buildMOOSE(swcfile):
    import loader_moose
    global chanDistrib_, passiveDistrib_
    global records_
    records_ = loader_moose.loadModel(swcfile, chanProto_, chanDistrib_, passiveDistrib_)
    compts = moose.wildcardFind('/model/##[TYPE=ZombieCompartment]')
    print("Total moose compartment: %s" % len(compts))

def runMOOSE():
    for i in range(10):
        moose.setClock(i, dt_)
    hsolve = moose.HSolve('/hsolve')
    hsolve.dt = dt_
    hsolve.target = '/model/##'
    moose.reinit()
    moose.start(0.1)
    records = {}
    mu.saveRecords(records_, outfile="moose_results.csv")

def main():
    global model_name_
    swcfile = sys.argv[1]
    model_name_ = os.path.basename(swcfile)
    compts = buildMOOSE(swcfile)
    runMOOSE()
    m2n.to_neuron('/model', outfile='%s.hoc' % model_name_)

if __name__ == '__main__':
    main()
