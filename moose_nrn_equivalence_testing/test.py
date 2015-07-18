import moose
import moose.utils as mu
from neuron import h
import sys
import pylab


def buildMOOSE(swcfile):
    import loader_moose
    records_ = loader_moose.loadModel(swcfile, None)
    compts = moose.wildcardFind('/model/##[TYPE=ZombieCompartment]')
    print("Total moose compartment: %s" % len(compts))
    moose.reinit()
    buildNRN(compts)

    #moose.start(0.1)
    #records = {}
    #for i, k in enumerate(records_):
    #    if i == 3:
    #        break
    #    else: records[k] = records_[k]
    #mu.plotRecords(records)

nrn_segs_ = {}
moose_compts_ = {}
soma_ = None
nrn_records_ = { 't' : h.Vector() }

def plotNrn():
    for i, k in enumerate(nrn_records_):
        pylab.plot(nrn_records_['t'], nrn_records_[k])
        if i == 5:
            break
    pylab.show()

def insertIntoNeuron(mooseCompt):
    global nrn_segs_
    global moose_compts_
    global soma_
    nrnSecName = mooseCompt.path.split('/')[-1]
    if mooseCompt.path in nrn_segs_:
        return nrn_segs_[mooseCompt.path]
    else:
        sec = h.Section()
        if not soma_:
            soma_ = sec
        sec.nseg = 1

        
        # inserting mechanism
        #for mech, gbar in [ ('na3', 120), ('kap', 36), ('pas', 0.001)]:
        #    h('%s insert %s' % (sec.hname(), mech))
        #    h('\tg_%s=%s' % (mech, gbar))

        
        sec.insert('na3')
        sec.insert('kap')
        sec.insert('pas')
        for seg in sec:
            seg.na3.gbar = 120
            seg.kap.gbar = 36
            #seg.pas.g = 0.001
        sec.L = mooseCompt.length * 1e6
        sec.diam = mooseCompt.diameter * 1e6
        nrn_segs_[mooseCompt.path] = sec
        moose_compts_[sec] = mooseCompt
        nrn_records_[nrnSecName] = h.Vector()
        nrn_records_[nrnSecName].record(sec(0.5)._ref_v)
        
        return sec

def buildNRN(mooseCompts):
    nrn_segs_ = {}
    moose_compts_ = {}
    from neuron import h
    for c in mooseCompts:
        cseg = insertIntoNeuron(c)
        # get the axial
        for i, cc in enumerate(c.neighbors['axial']):
            ccseg = insertIntoNeuron(cc)
            ccseg.connect(cseg)

    nrn_records_['t'].record(h._ref_t)

    h('access %s' % soma_.hname())
    h('objectvar stim')
    h('stim = new IClamp(0.5)')
    h('stim.amp = 1')
    h('stim.del = 0')
    h('stim.dur = 100')

    h.load_file('stdrun.hoc')
    h.init()
    h.tstop = 100
    h.run()
    plotNrn()

def main():
    swcfile = sys.argv[1]
    buildMOOSE(swcfile)

if __name__ == '__main__':
    main()
