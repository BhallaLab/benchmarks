
    //  This is a NEURON mod file generated from a ChannelML file

    //  Unit system of original ChannelML file: Physiological Units

COMMENT
    ChannelML file containing a single Channel description
ENDCOMMENT

TITLE Channel: nax

COMMENT
    Na channel for axon. Comment from original mod: Na current for axon. No slow inact. M.Migliore Jul. 1997, 
        added sh to account for higher threshold M.Migliore, Apr.2002
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

    SUFFIX nax
    USEION na READ ena WRITE ina VALENCE 1  // reversal potential of ion is read, outgoing current is written
           
        
    RANGE gmax, gion
    
    RANGE minf, mtau
    
    RANGE hinf, htau
    
}

PARAMETER { 

    gmax = 0.125 (S/cm2)  // default value, should be overwritten when conductance placed on cell
    
}



ASSIGNED {

    v (mV)
    
    celsius (degC)
    
        // Reversal potential of na
    ena (mV)
    // The outward flow of ion: na calculated by rate equations...
    ina (mA/cm2)
    
    
    gion (S/cm2)
    minf
    mtau (ms)
    hinf
    htau (ms)
    
}

BREAKPOINT { 
                        
    SOLVE states METHOD cnexp
    
    gion = gmax*((1*m)^3)*((1*h)^1)
    ina = gion*(v - ena)
            

}



INITIAL {
    
    ena = 50
        
    rates(v)
    m = minf
        h = hinf
        
    
}
    
STATE {
    m
    h
    
}

DERIVATIVE states {
    rates(v)
    m' = (minf - m)/mtau
    h' = (hinf - h)/htau
    
}

PROCEDURE rates(v(mV)) {  
    
    // Note: not all of these may be used, depending on the form of rate equations
    LOCAL  alpha, beta, tau, inf, gamma, zeta, temp_adj_m, A_alpha_m, B_alpha_m, Vhalf_alpha_m, A_beta_m, B_beta_m, Vhalf_beta_m, A_tau_m, B_tau_m, Vhalf_tau_m, temp_adj_h, A_alpha_h, B_alpha_h, Vhalf_alpha_h, A_beta_h, B_beta_h, Vhalf_beta_h, A_tau_h, B_tau_h, Vhalf_tau_h, A_inf_h, B_inf_h, Vhalf_inf_h
        
    TABLE minf, mtau,hinf, htau DEPEND celsius FROM -100 TO 100 WITH 2000
    
    
    UNITSOFF
    
                        // There is a Q10 factor which will alter the tau of the gates 
            
    temp_adj_m = 2^((celsius - 24)/10)
    temp_adj_h = 2^((celsius - 24)/10)
        
    //      ***  Adding rate equations for gate: m  ***
        
                    // Found a parameterised form of rate equation for alpha, using expression: A*((v-Vhalf)/B) / (1 - exp(-((v-Vhalf)/B)))
    A_alpha_m = 2.88
    B_alpha_m = 7.2
    Vhalf_alpha_m = -30 
    alpha = A_alpha_m * vtrap((v - Vhalf_alpha_m), B_alpha_m)
    
    
                    // Found a parameterised form of rate equation for beta, using expression: A*((v-Vhalf)/B) / (1 - exp(-((v-Vhalf)/B)))
    A_beta_m = 0.8928
    B_beta_m = -7.2
    Vhalf_beta_m = -30 
    beta = A_beta_m * vtrap((v - Vhalf_beta_m), B_beta_m)
    
     
                    // Found a generic form of the rate equation for tau, using expression: 1/( (alpha + beta) * temp_adj_m ) < 0.02 ? (0.02 * temp_adj_m) : 1/(alpha + beta) 
    
    
    if (1/( (alpha + beta) * temp_adj_m ) < 0.02 ) {
        tau =  (0.02 * temp_adj_m) 
    } else {
        tau =  1/(alpha + beta) 
    }
    mtau = tau/temp_adj_m
    minf = alpha/(alpha + beta)
          
       
    
       //     *** Finished rate equations for gate: m ***
    

    
        
    //      ***  Adding rate equations for gate: h  ***
        
                    // Found a parameterised form of rate equation for alpha, using expression: A*((v-Vhalf)/B) / (1 - exp(-((v-Vhalf)/B)))
    A_alpha_h = 0.045
    B_alpha_h = 1.5
    Vhalf_alpha_h = -45 
    alpha = A_alpha_h * vtrap((v - Vhalf_alpha_h), B_alpha_h)
    
    
                    // Found a parameterised form of rate equation for beta, using expression: A*((v-Vhalf)/B) / (1 - exp(-((v-Vhalf)/B)))
    A_beta_h = 0.015
    B_beta_h = -1.5
    Vhalf_beta_h = -45 
    beta = A_beta_h * vtrap((v - Vhalf_beta_h), B_beta_h)
    
     
                    // Found a generic form of the rate equation for tau, using expression: 1/( (alpha + beta) * temp_adj_h ) < 0.5 ? (0.5 * temp_adj_h) : 1/(alpha + beta) 
    
    
    if (1/( (alpha + beta) * temp_adj_h ) < 0.5 ) {
        tau =  (0.5 * temp_adj_h) 
    } else {
        tau =  1/(alpha + beta) 
    }
    htau = tau/temp_adj_h
     
                    // Found a generic form of the rate equation for inf, using expression: 1/(1 + (exp ((v-(-50))/4 )) )
    inf = 1/(1 + (exp ((v-(-50))/4 )) )
        
    hinf = inf
          
       
    
       //     *** Finished rate equations for gate: h ***
    

    
}


              // Function to assist with parameterised expressions of type linoid/exp_linear

FUNCTION vtrap(VminV0, B) {
    if (fabs(VminV0/B) < 1e-6) {
    vtrap = (1 + VminV0/B/2)
}else{
    vtrap = (VminV0 / B) /(1 - exp((-1 *VminV0)/B))
    }
}

UNITSON


