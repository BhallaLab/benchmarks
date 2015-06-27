def count_spikes(tables, threshold = 0.0):
    '''Count the number of spikes, also pupulate the spikeTables '''
    nSpikes = 0
    spikeBegin = False
    spikeEnds = False
    clock = moose.Clock('/clock')
    for tname in tables:
        t = tables[tname]
        dt = clock.currentTime / len(t.vector)
        spikeList = []
        for i, x in enumerate(t.vector):
            if x > threshold:
                if not spikeBegin:
                    spikeBegin = True
                    spikeEnds = False
                else: pass
            else:
                if spikeBegin:
                    spikeEnds = True
                    spikeBegin = False
                    spikeList.append(i*dt)
                    nSpikes += 1
        spikeTables[tname] = spikeList
    return nSpikes


def num_spikes(vec, threshold = 0.0):
    """Number of spikes in vector vec """
    nSpikes = 0
    spikeBegin = False
    spikeEnds = False
    spikeList = []
    for i, x in enumerate(vec):
        if x > threshold:
            if not spikeBegin:
                spikeBegin = True
                spikeEnds = False
            else: pass
        else:
            if spikeBegin:
                spikeEnds = True
                spikeBegin = False
                nSpikes += 1
    return nSpikes

