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

chanProto_ = [
        ['./cellMechanisms/KConductance/KChannel_HH.xml'], 
        ['./cellMechanisms/NaConductance/NaChannel_HH.xml'],
        ['./cellMechanisms/LeakConductance/LeakConductance.xml']
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
        ]

#chanDistrib = []
#for c in chanDistrib_:
#    print c
#    chanDistrib.append( c[0:3] + [ str(float(c[3])*15)])


def buildMOOSE(swcfile):
    import loader_moose
    global chanDistrib_, passiveDistrib_
    global records_
    records_ = loader_moose.loadModel(swcfile, chanProto_, chanDistrib_, passiveDistrib_)
    compts = moose.wildcardFind('/model/##[TYPE=ZombieCompartment]')
    print("Total moose compartment: %s" % len(compts))

def runMOOSE():
    for i in range(10):
        moose.setClock(i, 25e-6)
    moose.reinit()
    moose.start(0.1)
    records = {}
    for i, k in enumerate(records_):
        if i == 3:
            break
        else: records[k] = records_[k]
    mu.saveRecords(records_, outfile="moose_results.csv")

def plotNrn():
    for i, k in enumerate(nrn_records_):
        pylab.plot(nrn_records_['t'], nrn_records_[k])
        if i == 5:
            break
    pylab.show()


def main():
    global model_name_
    swcfile = sys.argv[1]
    model_name_ = os.path.basename(swcfile)
    compts = buildMOOSE(swcfile)
    runMOOSE()
    m2n.to_neuron('/model', outfile='%s.hoc' % model_name_)

if __name__ == '__main__':
    main()
