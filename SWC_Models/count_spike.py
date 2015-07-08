import numpy as np

def spikeLocation(vec, threshold):
    """Count the number of spikes in train, and return a list of index where
    spike ends.
    """

    nSpikes = 0
    spikeBegin, spikeEnds = False, False
    spikeList = []
    for i, x in enumerate(vec):
        if x > threshold:
            if not spikeBegin:
                spikeBegin, spikeEnds = True, False
            else: pass
        else:
            if spikeBegin:
                spikeEnds, spikeBegin = True, False
                spikeList.append(i)
                nSpikes += 1
    return nSpikes, spikeList

def spikes_characterization(vec, threshold = 0.0, dt = 50e-6):
    """Number of spikes in vector vec 
    mean of interval of spike occurance.
    variance of interval of spike occurance.
    """
    print("Spike characterization: theshold: {} and dt: {}".format(threshold ,
        dt))
    nSpikes, spikeList = spikeLocation(vec, threshold)
    if len(spikeList) > 1:
        diffIndex = np.diff(spikeList)
        meanDt = np.mean(diffIndex)
        varDt = np.var(diffIndex)
    else:
        meanDt = -1
        varDt = -1
    return nSpikes, meanDt, varDt


