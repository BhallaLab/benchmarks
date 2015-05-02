
?  This is a NEURON mod file generated from a ChannelML file

?  Unit system of original ChannelML file: Physiological Units

COMMENT
    ChannelML file containing a single Channel description
ENDCOMMENT

TITLE Channel: kap

COMMENT
    A type K channel. Comment from original mod: K-A channel from Klee Ficker and Heinemann,
        modified to account for Dax A Current --- M.Migliore Jun 1997,
        modified to be used with cvode  M.Migliore 2001
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

    SUFFIX kap
    USEION k READ ek WRITE ik VALENCE 1  ? reversal potential of ion is read, outgoing current is written
           
        
    RANGE gmax, gion
    
    RANGE ninf, ntau
    
    RANGE linf, ltau
    
}

PARAMETER { 

    gmax = 0.03 (S/cm2)  ? default value, should be overwritten when conductance placed on cell
    
}



ASSIGNED {

    v (mV)
    
    celsius (degC)
    
    ? Reversal potential of k
    ek (mV)
    ? The outward flow of ion: k calculated by rate equations...
    ik (mA/cm2)
    
    
    gion (S/cm2)
    ninf
    ntau (ms)
    linf
    ltau (ms)
    
}

BREAKPOINT { 
                        
    SOLVE states METHOD cnexp
    
    gion = gmax*((1*n)^1)*((1*l)^1)
    ik = gion*(v - ek)
            

}



INITIAL {
    
    ek = -90
        
    rates(v)
    n = ninf
        l = linf
        
    
}
    
STATE {
    n
    l
    
}

DERIVATIVE states {
    rates(v)
    n' = (ninf - n)/ntau
    l' = (linf - l)/ltau
    
}

PROCEDURE rates(v(mV)) {  
    
    ? Note: not all of these may be used, depending on the form of rate equations
    LOCAL  alpha, beta, tau, inf, gamma, zeta, temp_adj_n, A_alpha_n, B_alpha_n, Vhalf_alpha_n, A_beta_n, B_beta_n, Vhalf_beta_n, A_tau_n, B_tau_n, Vhalf_tau_n, A_inf_n, B_inf_n, Vhalf_inf_n, temp_adj_l, A_tau_l, B_tau_l, Vhalf_tau_l, A_inf_l, B_inf_l, Vhalf_inf_l
        
    TABLE ninf, ntau,linf, ltau DEPEND celsius FROM -100 TO 100 WITH 2000
    
    
    UNITSOFF
    
    ? There is a Q10 factor which will alter the tau of the gates 
            
    temp_adj_n = 5^((celsius - 24)/10)
                        
    temp_adj_l = 1
        
    ?      ***  Adding rate equations for gate: n  ***
         
    ? Found a generic form of the rate equation for alpha, using expression: (exp ( (1e-3 * (-1.5 + (-1)/(1 + (exp ((v-(-40))/5)))) * (v - 11) * 9.648e4) / (8.315*(273.16 + (celsius) )) ))
    alpha = (exp ( (1e-3 * (-1.5 + (-1)/(1 + (exp ((v-(-40))/5)))) * (v - 11) * 9.648e4) / (8.315*(273.16 + (celsius) )) ))
        
     
    ? Found a generic form of the rate equation for beta, using expression: (exp ( (1e-3 * (-1.5 + (-1)/(1 + (exp ((v-(-40))/5)))) * 0.55 * (v - 11) * 9.648e4) / (8.315*(273.16 + (celsius) )) ))
    beta = (exp ( (1e-3 * (-1.5 + (-1)/(1 + (exp ((v-(-40))/5)))) * 0.55 * (v - 11) * 9.648e4) / (8.315*(273.16 + (celsius) )) ))
        
     
    ? Found a generic form of the rate equation for tau, using expression: beta/(0.05 * (1 + alpha) * temp_adj_n) < 0.1 ? (0.1 * temp_adj_n) : beta/(0.05 * (1 + alpha)) 
    
    
    if (beta/(0.05 * (1 + alpha) * temp_adj_n) < 0.1 ) {
        tau =  (0.1 * temp_adj_n) 
    } else {
        tau =  beta/(0.05 * (1 + alpha)) 
    }
    ntau = tau/temp_adj_n
     
    ? Found a generic form of the rate equation for inf, using expression: 1/(1 + alpha)
    inf = 1/(1 + alpha)
        
    ninf = inf
          
       
    
    ?     *** Finished rate equations for gate: n ***
    

    
        
    ?      ***  Adding rate equations for gate: l  ***
         
    ? Found a generic form of the rate equation for tau, using expression: 0.26*(v + 50) < 2 ? 2 : 0.26*(v + 50)
    
    
    if (0.26*(v + 50) < 2 ) {
        tau =  2 
    } else {
        tau =  0.26*(v + 50)
    }
    ltau = tau/temp_adj_l
     
    ? Found a generic form of the rate equation for inf, using expression: 1/(1 + (exp ( (1e-3 * (3) * (v - (-56)) * 9.648e4) / (8.315*(273.16 + (celsius) )) )))
    inf = 1/(1 + (exp ( (1e-3 * (3) * (v - (-56)) * 9.648e4) / (8.315*(273.16 + (celsius) )) )))
        
    linf = inf
          
       
    
    ?     *** Finished rate equations for gate: l ***
    

    
}


UNITSON

