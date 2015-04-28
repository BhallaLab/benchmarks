
    //  This is a NEURON mod file generated from a ChannelML file

    //  Unit system of original ChannelML file: Physiological Units

COMMENT
    ChannelML file containing a single Channel description
ENDCOMMENT

TITLE Channel: kdr

COMMENT
    Delayed rectifier K channel. Comment from original mod: K-DR channel, from Klee Ficker and Heinemann,
        modified to account for Dax et al., M.Migliore 1997
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

    SUFFIX kdr
    USEION k READ ek WRITE ik VALENCE 1  // reversal potential of ion is read, outgoing current is written
           
        
    RANGE gmax, gion
    
    RANGE ninf, ntau
    
}

PARAMETER { 

    gmax = 0.01 (S/cm2)  // default value, should be overwritten when conductance placed on cell
    
}



ASSIGNED {

    v (mV)
    
    celsius (degC)
    
        // Reversal potential of k
    ek (mV)
    // The outward flow of ion: k calculated by rate equations...
    ik (mA/cm2)
    
    
    gion (S/cm2)
    ninf
    ntau (ms)
    
}

BREAKPOINT { 
                        
    SOLVE states METHOD cnexp
    
    gion = gmax*((1*n)^1)
    ik = gion*(v - ek)
            

}



INITIAL {
    
    ek = -90
        
    rates(v)
    n = ninf
        
    
}
    
STATE {
    n
    
}

DERIVATIVE states {
    rates(v)
    n' = (ninf - n)/ntau
    
}

PROCEDURE rates(v(mV)) {  
    
    // Note: not all of these may be used, depending on the form of rate equations
    LOCAL  alpha, beta, tau, inf, gamma, zeta, temp_adj_n, A_alpha_n, B_alpha_n, Vhalf_alpha_n, A_beta_n, B_beta_n, Vhalf_beta_n, A_tau_n, B_tau_n, Vhalf_tau_n, A_inf_n, B_inf_n, Vhalf_inf_n
        
    TABLE ninf, ntau DEPEND celsius FROM -100 TO 100 WITH 2000
    
    
    UNITSOFF
    temp_adj_n = 1
    
        
    //      ***  Adding rate equations for gate: n  ***
         
                    // Found a generic form of the rate equation for alpha, using expression: (exp ( (1e-3 * -3 * (v - 13) * 9.648e4) / (8.315*(273.16 + (celsius) )) ))
    alpha = (exp ( (1e-3 * -3 * (v - 13) * 9.648e4) / (8.315*(273.16 + (celsius) )) ))
        
     
                    // Found a generic form of the rate equation for beta, using expression: (exp ( (1e-3 * -3 * 0.7 * (v - 13) * 9.648e4) / (8.315*(273.16 + (celsius) ))) )
    beta = (exp ( (1e-3 * -3 * 0.7 * (v - 13) * 9.648e4) / (8.315*(273.16 + (celsius) ))) )
        
     
                    // Found a generic form of the rate equation for tau, using expression: beta/(0.02 * (1 + alpha)) < 2 ? 2 : beta/(0.02 * (1 + alpha)) 
    
    
    if (beta/(0.02 * (1 + alpha)) < 2 ) {
        tau =  2 
    } else {
        tau =  beta/(0.02 * (1 + alpha)) 
    }
    ntau = tau/temp_adj_n
     
                    // Found a generic form of the rate equation for inf, using expression: 1/(1 + alpha)
    inf = 1/(1 + alpha)
        
    ninf = inf
          
       
    
       //     *** Finished rate equations for gate: n ***
    

    
}


UNITSON


