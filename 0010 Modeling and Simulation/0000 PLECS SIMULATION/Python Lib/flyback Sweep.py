
#?----------------------------------------------------------------------------------------------------------------------------------------
#?                                      ______      __               __
#?                                     / __/ /_  __/ /_  ____ ______/ /__   ______      _____  ___  ____
#?                                    / /_/ / / / / __ \/ __ `/ ___/ //_/  / ___/ | /| / / _ \/ _ \/ __ \
#?                                   / __/ / /_/ / /_/ / /_/ / /__/ ,<    (__  )| |/ |/ /  __/  __/ /_/ /
#?                                  /_/ /_/\__, /_.___/\__,_/\___/_/|_|  /____/ |__/|__/\___/\___/ .___/
#?                                        /____/                                                /_/
#?                                  
#?----------------------------------------------------------------------------------------------------------------------------------------
import plecs as plc
import Model_Parameters as mdl
import numpy as np 
import post_process
import cleardata
import time
import os
#?----------------------------------------------------------------------------------------------------------------------------------------
port                                          = "1080"                                                               
url                                           = f"http://localhost:{port}/RPC2"                                      
modelname                                     = "flyback" 
mdlvar                                        = mdl.ModelVars
Vset                                          = (np.arange(5    ,24    +2    ,1    )).tolist()
Fs                                            = np.linspace(20e3, 250e3, num=len(Vset)).tolist()
plcsim                                        = plc.simpy(url=url , port=port , path=mdl.model_directory , modelvar=mdlvar)   
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim.rpc_connect()                                                                    
plcsim.load_model()
plcsim.ClearAllTraces(mdl.scopes)
cleardata.clear_data_folders()                                                                  
inc  = 0
for i, item1 in enumerate(Fs):
    for j, item2 in enumerate(Vset):

        utc_numeric                            = str(int(time.strftime("%Y%m%d%H%M%S",  time.gmtime() )))
        sim_idx                                = inc+1
        mdlvar['ToFile']['sim_idx']            = sim_idx
        mdlvar['ToFile']['utc_numeric']        = utc_numeric
        mdlvar['ToFile']['ToFile_path']        = str((os.path.join(mdl.current_directory,mdl.ToFile_path+f"Results_{utc_numeric}_{sim_idx}.csv")).replace("\\", "/"))
        mdlvar['ToFile']['logfile']            = str((os.path.join(mdl.current_directory,mdl.logfile_path+f"Log_{utc_numeric}_{sim_idx}.log")).replace("\\", "/"))
        mdlvar['ToFile']['output_html']        = str((os.path.join(mdl.current_directory,mdl.output_html_path+f"Html_{utc_numeric}_{sim_idx}.html")).replace("\\", "/"))
        mdlvar['ToFile']['Traces']             = str((os.path.join(mdl.current_directory,mdl.Traces_path)).replace("\\", "/"))
        mdlvar['CTRL']['Vset']                 = Vset[j]
        mdlvar['CTRL']['Fs']                   = Fs[i]

        plcsim.logParams(mdlvar['ToFile']['logfile'],mdlvar)
        plcsim.Set_sim_param(mdlvar)
        plcsim.launch_sim(modelname=modelname)
        # plcsim.HoldAllTraces(mdl.scopes)
        # plcsim.saveAllTraces(mdlvar['scopes'],mdl,mdlvar['ToFile']['Traces'])
        post_process.gen_plots(resFile= mdlvar['ToFile']['ToFile_path'], html_file=mdlvar['ToFile']['output_html'],OPEN=False)
        inc+=1
#?----------------------------------------------------------------------------------------------------------------------------------------


