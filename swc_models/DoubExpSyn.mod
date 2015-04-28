
?  This is a NEURON mod file generated from a ChannelML file

?  Unit system of original ChannelML file: Physiological Units

COMMENT
    ChannelML file describing a single synaptic mechanism
ENDCOMMENT

? Creating synaptic mechanism, based on NEURON source impl of Exp2Syn
    

TITLE Channel: DoubExpSyn

COMMENT
    Simple example of a synaptic mechanism, which consists of a postsynaptic conductance which changes as 
        double exponential function of time. Mappings exist for NEURON and GENESIS.
ENDCOMMENT


UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

    
NEURON {
    POINT_PROCESS DoubExpSyn
    RANGE tau_rise, tau_decay 
    GLOBAL total
    


    RANGE i, e, gmax
    NONSPECIFIC_CURRENT i
    RANGE g, factor

}

PARAMETER {
    gmax = 0.01
    tau_rise = 1 (ms) <1e-9,1e9>
    tau_decay = 2 (ms) <1e-9,1e9>
    e = 0  (mV)

}


ASSIGNED {
    v (mV)
    i (nA)
    g (uS)
    factor 
    total (uS)

}

STATE {
    A (uS)
    B (uS)
}

INITIAL {
    LOCAL tp
    total = 0
    
    if (tau_rise == 0) {
        tau_rise = 1e-9  : will effectively give a single exponential timecourse synapse
    }
    
    if (tau_rise/tau_decay > .999999) {
        tau_rise = .999999*tau_decay : will result in an "alpha" synapse waveform
    }
    A = 0
    B = 0
    tp = (tau_rise*tau_decay)/(tau_decay - tau_rise) * log(tau_decay/tau_rise)
    factor = -exp(-tp/tau_rise) + exp(-tp/tau_decay)
    factor = 1/factor
}

BREAKPOINT {
    SOLVE state METHOD cnexp
    g = gmax * (B - A)
    i = g*(v - e)
    
}


DERIVATIVE state {
    A' = -A/tau_rise
    B' = -B/tau_decay 
}

NET_RECEIVE(weight (uS)) {
    
    state_discontinuity(A, A + weight*factor)
    state_discontinuity(B, B + weight*factor)

    
    
}

