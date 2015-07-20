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
    text.append("}\n\n")
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
    context.append("\n")
    return "\n".join(context)

def insert_pulsegen(stim):
    stimname = nrn_name(stim)
    text = []
    text.append('\nobjectvar %s' % stimname)
    for comptVecs in stim.neighbors['output']:
        for compt in comptVecs:
            targetName = nrn_name(compt)
            text.append("%s %s = new IClamp(0.5)" % (targetName, stimname)) 
            text.append("%s.amp = %s" % (stimname, stim.level[0] * 1e9))
            text.append("%s.del = %s" % (stimname, stim.delay[0] * 1e3))
            text.append("%s.dur = %s" % (stimname, (stim.delay[0] + stim.width[0])*1e3))
    return "\n".join(text)+"\n"

def insert_record(index, table):
    text = []
    tableName = "%s_%s" % (nrn_name(table), index)
    text.append('objref rect')
    text.append('rect = new Vector()')
    text.append('rect.record(&t)')
    for targetVecs in table.neighbors['requestOut']:
        for target in targetVecs:
            targetName = nrn_name(target)
            text.append("objref %s" % tableName)
            text.append("%s = new Vector()" % tableName)
            text.append('%s.record(&%s.v(0.5))'%(tableName, targetName)) 
    return "\n".join(text), tableName

def stimulus_text():
    stimtext = [ 'load_file("stdrun.hoc")' ]
    mu.info(" Default sim time is 1 second. Change it in script.")
    stimtext.append('tstop=%s' % 1000)
    stimtext.append('cvode.active(1)')
    stimtext.append('finitialize()')
    stimtext.append('run()')
    stimtext.append("\n")
    stimtext = "\n".join(stimtext)
    return stimtext

def plot_text(tableList):
    plottext = ["objref outF"]
    plottext.append("outF = new File()")
    plottext.append('outF.wopen("nrn_out.dat")')
    plottext.append('outF.printf("t,%s")' % ",".join(tableList))
    plottext.append('for i=0,rect.size()-1 {\n')
    glist, plotlist = ["%g"], ["rect.x(i)"]
    for t in tableList:
        glist.append("%g")
        plotlist.append("%s.x(i)" % t)
    plottext.append('\toutF.printf("%s\\n", %s)' % (" ".join(glist), ",".join(plotlist)))
    plottext.append("}")
    plottext.append("\n")
    return "\n".join(plottext)


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

    pulsetext = []
    for stim in  moose.wildcardFind('%s/##[TYPE=PulseGen]' % path):
        pulsetext.append(insert_pulsegen(stim))

    recordText, tableList = [], []
    for i, table in enumerate(moose.wildcardFind('%s/##[TYPE=Table]' % path)):
        text, tableName = insert_record(i, table)
        recordText.append(text)
        tableList.append(tableName)

    stimtext = stimulus_text()
    plottext = plot_text(tableList)
    
    outfile = kwargs.get('outfile', 'moose_to_neuron.hoc')
    mu.info("Writing neuron model to %s" % outfile)
    with open(outfile, "w") as f:
        f.writelines(headerText)
        f.writelines(comptText)
        f.writelines(connectionText)
        f.writelines(recordText)
        f.writelines(pulsetext)
        f.writelines(stimtext)
        f.writelines(plottext)
