
    //  This is a NEURON mod file generated from a ChannelML file

    //  Unit system of original ChannelML file: Physiological Units

COMMENT
    ChannelML file containing a single Channel description
ENDCOMMENT

TITLE Channel: hd

COMMENT
    H current. Comment from original mod: I-h channel from Magee 1998 for distal dendrites
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

    SUFFIX hd
    USEION hd READ ehd WRITE ihd VALENCE 1  // reversal potential of ion is read, outgoing current is written
           
        
    RANGE gmax, gion
    
    RANGE linf, ltau
    
    RANGE vhalfl
}

PARAMETER { 

    gmax = 5e-05 (S/cm2)  // default value, should be overwritten when conductance placed on cell
    
    vhalfl = -81 : Note units of this will be determined by its usage in the generic functions

}



ASSIGNED {

    v (mV)
    
    celsius (degC)
    
        // Reversal potential of hd
    ehd (mV)
    // The outward flow of ion: hd calculated by rate equations...
    ihd (mA/cm2)
    
    
    gion (S/cm2)
    linf
    ltau (ms)
    
}

BREAKPOINT { 
                        
    SOLVE states METHOD cnexp
    
    gion = gmax*((1*l)^1)
    ihd = gion*(v - ehd)
            

}



INITIAL {
    
    ehd = -30
        
    rates(v)
    l = linf
        
    
}
    
STATE {
    l
    
}

DERIVATIVE states {
    rates(v)
    l' = (linf - l)/ltau
    
}

PROCEDURE rates(v(mV)) {  
    
    // Note: not all of these may be used, depending on the form of rate equations
    LOCAL  alpha, beta, tau, inf, gamma, zeta, temp_adj_l, A_tau_l, B_tau_l, Vhalf_tau_l, A_inf_l, B_inf_l, Vhalf_inf_l
        
    TABLE linf, ltau DEPEND celsius, vhalfl FROM -100 TO 100 WITH 2000
    
    
    UNITSOFF
    
                        // There is a Q10 factor which will alter the tau of the gates 
            
    temp_adj_l = 4.5^((celsius - 33)/10)
        
    //      ***  Adding rate equations for gate: l  ***
         
                    // Found a generic form of the rate equation for tau, using expression: (exp (0.033264 * (v - (-75))))/(0.011 * (1 + (exp (0.08316 * (v - (-75)))))) 
    tau = (exp (0.033264 * (v - (-75))))/(0.011 * (1 + (exp (0.08316 * (v - (-75)))))) 
        
    ltau = tau/temp_adj_l
     
                    // Found a generic form of the rate equation for inf, using expression: 1/(1 + (exp (- (v-(vhalfl))/ (-8) )) )
    inf = 1/(1 + (exp (- (v-(vhalfl))/ (-8) )) )
        
    linf = inf
          
       
    
       //     *** Finished rate equations for gate: l ***
    

    
}


UNITSON


