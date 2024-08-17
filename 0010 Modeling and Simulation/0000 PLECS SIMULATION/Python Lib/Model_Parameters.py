
#!---------------------------------------------------------------------------------------------------------------------------------------- 
#!                                      ______      __               __
#!                                     / __/ /_  __/ /_  ____ ______/ /__   _   ______ ___________
#!                                    / /_/ / / / / __ \/ __ `/ ___/ //_/  | | / / __ `/ ___/ ___/
#!                                   / __/ / /_/ / /_/ / /_/ / /__/ ,<     | |/ / /_/ / /  (__  )
#!                                  /_/ /_/\__, /_.___/\__,_/\___/_/|_|    |___/\__,_/_/  /____/
#!                                        /____/
#!                                  
#!----------------------------------------------------------------------------------------------------------------------------------------
import os 
import time 
#!----------------------------------------------------------------------------------------------------------------------------------------                                                         
current_directory   = os.getcwd()                                                                                                                                                              
Traces_path         = "0010 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Traces/"           
ToFile_path         = "0010 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/CSV/"              
logfile_path        = "0010 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Log/"              
output_html_path    = "0010 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/html/"             
model_path          = "0010 Modeling and Simulation/0000 PLECS SIMULATION/Model/flyback.plecs"                  
model_directory     = (os.path.join(current_directory, model_path)).replace("\\", "/")                                        
#!----------------------------------------------------------------------------------------------------------------------------------------
Sim_param 	= {                                                                                            
                  'tSim'	    	   : 0.05,                                                                 #? [s]     - Total simulation time
                  'load_tflip'	   : 0.05*   0.5,                                                          #? [s]     - Time at which the load changes state 
                  'maxStep'		   : 1e-3,                                                                 #? [s]     - Maximum simulation time step
                  'ZeroCross'       : 1000,                                                                 #? [/]     - Zero-crossing detection limit
                  'rel_tol'		   : 1e-7                                                                  #? [/]     - Relative tolerance for the numerical solver
               }
ToFile      = {   
                  'Ts'              : 10e-6,                                                                #? [s]     - Sampling time for saving data
                  'tsave' 	    	   : Sim_param['tSim']-0                                                   #? [s]     - Time point at which the data is saved
               }  
SW          = {                                                                                             
                  'Config'          : 1,                                                                    #? [/]      - Switch configuration 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   #? [/]      - MOSFET thermal model file path
                  'Rgon'            : 2.5,                                                                  #? [Ohm]    - Gate resistance for turn-on 
                  'Rgoff'           : 2.5,                                                                  #? [Ohm]    - Gate resistance for turn-off
                  'ron_mosfet'      : 0.04,                                                                 #? [Ohm]    - MOSFET on-state resistance 
                  'Iinit'           : 0,                                                                    #? [A]      - Initial current through the MOSFET 
                  'Coss'            :  {                                                                                           
                                          'Config'		      : 5,                                            #? [/]      - Capacitance configuration
                                          'Cap_s'    		   : 1e-12,                                        #? [F]      - Capacitance value 
                                          'Resr_s'		      : 0,                                            #? [F]      - Equivalent series resistance of the capacitance
                                          'Lesl_s'		      : 0,                                            #? [H]      - Equivalent series inductance of the capacitance
                                          'Npara'		      : 1,                                            #? [/]      - Number of parallel capacitors
                                          'Nseri'		      : 1,                                            #? [/]      - Number of series capacitors
                                          'Vinit'		      : 0,                                            #? [V]      - Initial voltage across the capacitance
                                          'Iinit'		      : 0                                             #? [A]      - Initial current through the capacitance      
                                          },                                                               
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         #? [/]      - Body diode thermal model file path
                  'ron_body_diode'  : 5e-3,                                                                 #? [Ohm]    - Body diode on-state resistance 
                  'Rdb_off'         : 0,                                                                    #? [Ohm]    - Resistance when the body diode is off 
                  'vf_body_diode'   : 0.6,                                                                  #? [V]      - Body diode forward voltage 
                  'nPara'           : 1,                                                                    #? [/]      - Number of parallel MOSFETs
                  'T_init'          : 25,                                                                   #? [°C]     - Initial temperature of the MOSFET 
                  'Tamb'            : 25,                                                                   #? [°C]     - Ambient temperature 
                  't_init'          : 25,                                                                   #? [/]      - Initial time for thermal calculations 
                  'rth_sw'          : 0.09,                                                                 #? [K/W]    - Thermal resistance between the switch junction and case 
                  'rth_ch'          : 0.5,                                                                  #? [K/W]    - Thermal resistance between the case and heatsink 
                  'Rth'             : 0.34 	                                                               #? [K/W]    - Total thermal resistance 				    	                           
               }
Trafo       = {                                                                                             
                  'eq_per_leak'     : 5.9e-9,                                                               #? [H]      - Equivalent primary leakage inductance 
                  'MMF_leak'        : 0,                                                                    #? [A·t]    - MagnetoMotive Force (MMF) leakage 
                  'NP'              : 13,                                                                   #? [/]      - Number of primary turns
                  'NS'              : 7,                                                                    #? [/]      - Number of secondary turns
                  'NS2'             : 3,                                                                    #? [/]      - Number of secondary turns for the second winding
                  'CSA_core'		   : 9.39e-5,                                                              #? [m^2]    - Core cross-sectional area 
                  'Lflux_core'		: 0.0376,                                                               #? [V·s]    - Core flux linkage 
                  'rel_per_core'		: 9550,                                                                 #? [V]      - Relative permeability of the core material
                  'Sat_per_core'		: 1,                                                                    #? [K/W]    - Saturation permeability of the core material    
                  'flux_dens_core'  : 0.47,                                                                 #? [T]      - Magnetic flux density in the core 
                  'MMF_core'		   : 0,                                                                    #? [A·t]    - MagnetoMotive Force (MMF) in the core 
                  'CSA_gap'		   : 9.39e-5,                                                              #? [m^2]    - Air gap cross-sectional area 
                  'Lflux_gap'		   : 0.00022,                                                              #? [V·s]    - Air gap flux linkage 
                  'MMF_gap'		   : 0                                                                     #? [A·t]    - MagnetoMotive Force (MMF) in the air gap 
               }	

Cout        = {                                                                                             
                  'Config'		      : 1,                                                                    #? [/]      - Configuration of the output capacitor
                  'Cap_s'    		   : 220e-6,                                                               #? [F]      - Capacitance value  
                  'Resr_s'	         : 19e-9,                                                                #? [Ohm]    - Equivalent series resistance of the capacitor 
                  'Lesl_s'	         : 1e-19,                                                                #? [H]      - Equivalent series inductance of the capacitor 
                  'Npara'		      : 1,                                                                    #? [/]      - Number of parallel capacitors
                  'Nseri'		      : 1,                                                                    #? [/]      - Number of series capacitors
                  'Vinit'		      : 0,                                                                    #? [V]      - Initial voltage across the capacitor 
                  'Iinit'		      : 1e-3                                                                  #? [A]      - Initial current through the capacitor 
               }
Load        = {                                                                                             
                  'Config'		      : 1,                                                                    #? [/]      - Load configuration
                  'CL'    		      : 0,                                                                    #? [F]      - Load capacitance 
                  'RL'		         : 5,                                                                    #? [Ohm]    - Load resistance 
                  'LL'		         : 0,                                                                    #? [H]      - Load inductance 
                  'Vinit'		      : 0,                                                                    #? [V]      - Initial voltage across the load 
                  'Iinit'		      : 0,                                                                    #? [A]      - Initial current through the load 
                  't_switch'        : Sim_param['tSim']-Sim_param['load_tflip'],                            #? [s]      - Load switch timing 
                  't_dead'          : (Sim_param['tSim']-Sim_param['load_tflip'])/2,                        #? [s]      - Dead time for load switching 
                  'Pout'		      : 30,                                                                   #? [W]      - Desireed output power
                  'Vout1'		      : 12,                                                                   #? [V]      - Desiered output voltage 
                  'Vout2'		      : 5                                                                     #? [V]      - Desiered output voltage 
               }
CTRL        = {                                                                                             
                  'Vset'    		   :  Load['Vout1']                                                        #? [V]      - Voltage set point for control 
                 
               }
RCD         = {                                                                                             
                  'R'               : 1e5,                                                                  #? [Ohm]    - Resistor value in the RCD snubber 
                  'C'               : 1e-6,                                                                 #? [F]      - Capacitor value in the RCD snubber 
                  'diode'		      : 'file:C4D40120D',                                                     #? [/]      - Diode model file path
                  'ron_diode'		   : 0.6,                                                                  #? [Ohm]    - Diode on-state resistance 
                  'vf_diode'		   : 0.6,                                                                  #? [V]      - Diode forward voltage 
                  'rth_ch_diode'		: 0.5,                                                                  #? [K/W]    - Diode thermal resistance (junction-to-case)       
                  'num_par_diode'	: 1,                                                                    #? [/]      - Number of parallel diodes
                  'rth_ch'		      : 0.1,                                                                  #? [K/W]    - Heatsink-to-ambient thermal resistance 
                  't_init'		      : 25                                                                    #? [°C]     - Initial temperature of the diode 
               }
RC_snub     = {                                                                                             
                  'Rsnub'           : 10  ,                                                                  #? [Ohm]    - Resistor value in the RC snubber
                  'Csnub'           :  {                                                                                           
                                          'Config'		      : 2,                                            #? [/]      - Configuration of the snubber capacitor
                                          'Cap_s'    		   : 8e-06,                                        #? [F]      - Snubber capacitance value 
                                          'Resr_s'		      : 1e-5,                                         #? [Ohm]    - Equivalent series resistance of Csnub 
                                          'Lesl_s'		      : 0,                                            #? [H]      - Equivalent series inductance of Csnub 
                                          'Npara'		      : 1,                                            #? [/]      - Number of parallel snubber capacitors
                                          'Nseri'		      : 1,                                            #? [/]      - Number of series snubber capacitors
                                          'Vinit'		      : 0,                                            #? [V]      - Initial voltage across Csnub 
                                          'Iinit'		      : 0                                             #? [A]      - Initial current through Csnub       
                                          },    
               }
diode       = {
                  'diode'		         : 'file:C4D40120D',                                                  #? [/]      - Diode model file path       
                  'ron_diode'		      : 0.04,                                                              #? [Ohm]    - Diode on-state resistance 
                  'vf_diode'		      : 0.6,                                                               #? [V]      - Diode forward voltage 
                  'rth_ch_diode'		   : 0.5,                                                               #? [K/W]    - Diode thermal resistance (junction-to-case)      
                  'num_par_diode'		: 1,                                                                 #? [/]      - Number of parallel diodes
                  'Rth'		            : 0.1,                                                               #? [K/W]    - Heatsink-to-ambient thermal resistance 
                  't_init'		         : 25                                                                 #? [°C]     - Initial temperature of the diode 
               }
Thermals    = {                                                                                             
                  'T_amb'           :  25.0,                                                                #? [°C]     - Ambient temperature 
                  'rth_Amb'         :  0.09                                                                 #? [K/W]    - Thermal resistance from case to ambient 
               }

#!----------------------------------------------------------------------------------------------------------------------------------------
ModelVars   = {                                                                                             
                  'Sim_param'       :  Sim_param   ,      
                  'ToFile'          :  ToFile      ,    
                  'SW'              :  SW          ,                                                             
                  'Trafo'           :  Trafo       ,                                                                 
                  'CTRL'            :  CTRL        ,                                                            
                  'Cout'            :  Cout        ,  
                  'Load'            :  Load        ,                                                                
                  'RCD'             :  RCD         ,    
                  'RC_snub'         :  RC_snub     ,                                                                                                                            
                  'diode'           :  diode       ,                                                                
                  'Thermals'        :  Thermals    ,
               }	
#!----------------------------------------------------------------------------------------------------------------------------------------	
scopes      =  [                                                                                            
				      "flyback/Scopes/input",                                                                 
				      "flyback/Scopes/RCD",                                                                                         
				      "flyback/Scopes/load_scope",                                                                                         
				      "flyback/Scopes/load_scope1",                                                                                        
				      "flyback/Scopes/MMF",                                                                                      
				      "flyback/Scopes/primary",                                                                                    
				      "flyback/Scopes/secondary1",                                                                                    
				      "flyback/Scopes/secondary2",                                                                                    
				      "flyback/Scopes/Mos",                                                                                  
				      "flyback/Scopes/diodes",                                                                                
				      "flyback/Scopes/cout",                                                                                
				      "flyback/Scopes/Power",                                                                                 
				      "flyback/Scopes/Outputs",                                                                                
				      "flyback/Scopes/PI"                                                                                 
               ]	
Waveforms   =  [                                                                                            
                  'Source Voltage',                  
                  'Source Current',
                  'Source Power',
                  #!-------------------------
                  'RCD Clamp Current',
                  'RCD C Current',
                  'RCD R Current',
                  'RCD Clamp Voltage',                  
                  'RCD C Voltage',                  
                  'RCD R Voltage',                  
                  'RCD Clamp Dissipation',
                  #!-------------------------
                  'Load1 Voltage',
                  'Load1 Current',
                  #!-------------------------
                  'Load2 Voltage',
                  'Load2 Current',
                  #!-------------------------
                  'Core Field Strength',
                  'Core Flux Density',
                  'Air gap Field Strength',
                  'Air gap Flux Density',
                  #!-------------------------
                  'Core MMF',
                  'Core Flux',
                  'Air gap MMF',
                  'Air gap Flux',
                  #!-------------------------
                  'Primary Winding voltage',
                  'Primary Winding Current',
                  'Secondary1 Winding voltage',
                  'Secondary1 Winding Current',
                  'Secondary2 Winding voltage',
                  'Secondary2 Winding Current',
                  #!-------------------------
                  'MOSFET voltage',
                  'BD voltage',
                  'MOSFET Current',
                  'BD Current',
                  'MOSFET junction Temp',
                  'BD junction Temp',
                  'MOSFET case Temp',
                  'MOSFET switching losses',
                  'BD switching losses',
                  'MOSFET conduction losses',
                  'BD conduction losses',
                  #!-------------------------
                  'Diode1 voltage',
                  'Diode1 Current',
                  'Diode1 junction Temp',
                  'Diode1 case Temp',
                  'Diode1 switching losses',
                  'Diode1 Diode LS1 junction Temp',
                  'Diode1 conduction losses',

                  'Diode2 voltage',
                  'Diode2 Current',
                  'Diode2 junction Temp',
                  'Diode2 case Temp',
                  'Diode2 switching losses',
                  'Diode2 Diode LS1 junction Temp',
                  'Diode2 conduction losses',
                  #!-------------------------
                  'Cout1 Voltage',                  
                  'Cout1 Current',
                  'Cout1 Dissipation',
                  #!-------------------------
                  'Cout2 Voltage',                  
                  'Cout2 Current',
                  'Cout2 Dissipation',
                  #!-------------------------                 
                  'Power',
                  'Vout',
                  'Iout',
                  'Vout2',
                  'Iout2',
                  'Total Power Loss',
                  'Input Power',
                  'Output Power',
                  'Efficiency'
               ]		
Units       =  [                                                                                            
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ W ]',                  
                  #!-------------------------
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ V ]',                  
                  '[ V ]',                  
                  '[ V ]',                  
                  '[ W ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                                  
                  #!-------------------------
                  '[A/m]',
                  '[Wb/m²]',
                  '[A/m]',
                  '[Wb/m²]',
                  #!-------------------------
                  '[A·turns]',
                  '[Wb]',
                  '[A·turns]',
                  '[Wb]',
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ V ]',                  
                  '[ A ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ W ]',                  
                  '[ C ]',                  
                  '[ W ]',                  
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ W ]',                  
                  '[ C ]',                  
                  '[ W ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ W ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ W ]',                  
                  #!-------------------------                 
                  '[ W ]',                  
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ V ]',                  
                  '[ A ]',               
                  '[ W ]',   
                  '[ W ]', 
                  '[ W ]',               
                  '[ % ]',                   
               ]
#!----------------------------------------------------------------------------------------------------------------------------------------	
