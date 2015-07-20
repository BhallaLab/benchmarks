#!/usr/bin/env python

import os
import moose
import moose.utils as mu
import sys
import pylab
from collections import defaultdict

nrn_segs_ = {}
moose_compts_ = {}
soma_ = None
nrn_text_ = {} #defaultdict(list)
model_name_ = None

passiveDistrib_ = [ 
        [ ".", "#", "RM", "2.8", "CM", "0.01", "RA", "1.5",  
            "Em", "-58e-3", "initVm", "-65e-3" ]
        , [ ".", "#axon#", "RA", "0.5" ] 
        ]

chanDistrib_ = [
        [  "na3", "#", "Gbar", "1200" ]
        , [ "nax", "#", "Gbar", "125" ]
        , [ "kap", "#", "Gbar", "360" ]
        , [ "kdr", "#", "Gbar", "10" ]
        , [ "hd", "#", "Gbar", "0.05" ]
        , [ "kad", "#", "Gbar", "60" ]
        ]


def buildMOOSE(swcfile):
    import loader_moose
    global chanDistrib_, passiveDistrib_
    records_ = loader_moose.loadModel(swcfile, chanDistrib_, passiveDistrib_)
    compts = moose.wildcardFind('/model/##[TYPE=ZombieCompartment]')
    print("Total moose compartment: %s" % len(compts))
    moose.reinit()
    #moose.start(0.1)
    #records = {}
    #for i, k in enumerate(records_):
    #    if i == 3:
    #        break
    #    else: records[k] = records_[k]
    #mu.plotRecords(records)
    return compts

def plotNrn():
    for i, k in enumerate(nrn_records_):
        pylab.plot(nrn_records_['t'], nrn_records_[k])
        if i == 5:
            break
    pylab.show()

def nrnName(compt):
    assert type(compt) != moose.vec, compt
    path = compt.path
    path = path.split('/')[-1]
    return path.translate(None, "[]/")

def insertIntoNeuron(mooseCompt):
    global nrn_segs_
    global moose_compts_
    global soma_

    secname = nrnName(mooseCompt)
    text = [ "create %s" % secname ]

    params = [ "%s { " % secname ]

    # Here we fill in the mechanism.
    params += [ "nseg = 1" ]

    for chan in chanDistrib_:
        mech, x, y, gbar = chan
        params.append('insert %s { gmax = %s }' % (mech, float(gbar)/10.0))

    text.append("\n\t".join(params))
    text.append("}")
    return "\n".join(text)

def connectSec(compt):
    global nrn_text_
    srcSec = nrnName(compt)
    context = []
    neighbours = compt.neighbors['axial']
    for c in neighbours:
        for tgt in c:
            tgtSec = nrnName(tgt)
            context.append('connect %s(0), %s(1)' % (tgtSec, srcSec))
    return "\n".join(context)

def mooseToNrn(compts):
    """Create a neuron script """
    global nrn_text_, model_name_

    nrn_text_['header'] = 'load_file("stdrun.hoc")'

    networkText = []
    for c in compts:
        networkText.append(insertIntoNeuron(c))
    nrn_text_['build_network'] = "\n".join(networkText)

    connectionText = []
    for c in compts:
        connectionText.append(connectSec(c))
    nrn_text_['connections'] = "\n".join(connectionText) 

    with open("%s.hoc" % model_name_, "w") as f:
        f.write(nrn_text_['header'])
        f.write("\n")
        f.write(nrn_text_['build_network'])
        f.write("\n")
        f.write(nrn_text_['connections'])
        f.write("\n")


def main():
    global model_name_
    swcfile = sys.argv[1]
    model_name_ = os.path.basename(swcfile)
    compts = buildMOOSE(swcfile)
    mooseToNrn(compts)

if __name__ == '__main__':
    main()
