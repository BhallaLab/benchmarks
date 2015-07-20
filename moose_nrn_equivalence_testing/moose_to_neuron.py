"""moose_to_neuron.py: 

Convert moose model to NEURON.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import moose
import moose.utils as mu

compts_ = set()
nrn_txt_ = {}

def nrn_name(compt):
    assert type(compt) != moose.vec, compt
    path = compt.path
    path = path.split('/')[-1]
    return path.translate(None, "[]/")

def create_section_in_neuron(mooseCompt):
    secname = nrn_name(mooseCompt)
    text = [ "create %s" % secname ]
    params = [ "%s { " % secname ]
    # Here we fill in the mechanism.
    params += [ "nseg = 1" ]

    channels = mooseCompt.neighbors['channel']
    for chanVec in channels:
        for chan in chanVec:
            mech = chan.name
            gbar, ek = chan.Gbar, chan.Ek
            params.append('insert {0} {{ gbar_{0} = {1:.4f} ek_{0} = {2:.4f} }}'.format(
                mech
                , float(gbar) * 1e6
                , float(ek) * 1e3)
            )
    text.append("\n\t".join(params))
    text.append("}")
    return "\n".join(text)

def connect_neuron_sections(compt):
    global nrn_text_
    srcSec = nrn_name(compt)
    context = []
    neighbours = compt.neighbors['axial']
    for c in neighbours:
        for tgt in c:
            tgtSec = nrn_name(tgt)
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
        connectionText.append(connect_neuron_sections(c))
    nrn_text_['connections'] = "\n".join(connectionText) 

def insert_pulsegen(stim):
    stimname = nrn_name(stim)
    text = []
    text.append('objectvar %s' % stimname)
    for comptVecs in stim.neighbors['output']:
        for compt in comptVecs:
            targetName = nrn_name(compt)
            text.append("%s %s = new IClamp(0.5)" % (targetName, stimname)) 
            text.append("%s.amp = %s" % (stimname, stim.level[0] * 1e9))
            text.append("%s.del = %s" % (stimname, stim.delay[0] * 1e3))
            text.append("%s.dur = %s" % (stimname, (stim.delay[0] + stim.width[0])*1e3))
    return "\n".join(text)
            

def insert_record(index, table):
    text = []
    tableName = "%s_%s" % (nrn_name(table), index)
    for targetVecs in table.neighbors['requestOut']:
        for target in targetVecs:
            targetName = nrn_name(target)
            text.append("objref %s" % tableName)
            text.append("%s = new Vector()" % tableName)
            text.append('%s.record(&%s.v(0.5))'%(tableName, targetName)) 
    return "\n".join(text)


def to_neuron(path, **kwargs):
    moose.reinit()
    mooseCompts = moose.wildcardFind('%s/##[TYPE=Compartment]' % path)
    zombiles = moose.wildcardFind('%s/##[TYPE=ZombieCompartment]'% path)
    compts = set(mooseCompts).union(set(zombiles))

    headerText = []

    comptText = []
    for c in compts:
        comptText.append(create_section_in_neuron(c))

    connectionText = []
    for c in compts:
        connectionText.append(connect_neuron_sections(c))

    stimText = []
    for stim in  moose.wildcardFind('%s/##[TYPE=PulseGen]' % path):
        stimText.append(insert_pulsegen(stim))

    recordText = []
    for i, table in enumerate(moose.wildcardFind('%s/##[TYPE=Table]' % path)):
        recordText.append(insert_record(i, table))

    stimtext = [ 'load_file("stdrun.hoc")' ]
    mu.info("Default sim time is 1 second. Change it in script.")
    stimtext.append('tstop=%s' % 1000)
    stimtext.append('run()')

    plottext = ["objref outF"]
    plottext.append("outF = new File()")
    plottext.append('outF.wopen("nrn_out.dat")')

    outfile = kwargs.get('outfile', 'moose_to_neuron.hoc')
    mu.info("Writing neuron model to %s" % outfile)
    with open(outfile, "w") as f:
        f.write("\n".join(headerText))
        f.write("\n")
        f.write("\n".join(comptText))
        f.write("\n")
        f.write("\n".join(connectionText))
        f.write("\n")
        f.write("\n".join(recordText))
        f.write("\n".join(stimText))
        f.write("\n")
        f.write("\n".join(plottext))
