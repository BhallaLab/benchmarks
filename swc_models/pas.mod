
    //  This is a NEURON mod file generated from a ChannelML file

    //  Unit system of original ChannelML file: Physiological Units

COMMENT
    ChannelML file containing a single Channel description
ENDCOMMENT

TITLE Channel: pas

COMMENT
    Simple example of a leak/passive conductance. Note: for GENESIS cells with a single leak conductance,
        it is better to use the Rm and Em variables for a passive current.
ENDCOMMENT


UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
    (um) = (micrometer)
    (molar) = (1/liter)
    (mM) = (millimolar)
    (l) = (liter)
}


    
NEURON {

    SUFFIX pas
        // A non specific current is present
    RANGE e
    NONSPECIFIC_CURRENT i
    
    RANGE gmax, gion
    
}

PARAMETER { 

    gmax = 3.57143e-05 (S/cm2)  // default value, should be overwritten when conductance placed on cell
    
    e = -58 (mV) // default value, should be overwritten when conductance placed on cell
    
}



ASSIGNED {

    v (mV)
        
    i (mA/cm2)
        
}

BREAKPOINT { 
    i = gmax*(v - e) 
        

}


