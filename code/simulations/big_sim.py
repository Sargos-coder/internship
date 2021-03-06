''' big_sim.py
'''

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from brian2 import clear_cache, uA, mV, ms
from models.models import Barrel_PC, Barrel_IN
from foundations.helpers import scale_to_freq
from foundations.make_dynamic_experiments import make_dynamic_experiments
import numpy as np
import pandas as pd

# Set Parameters
baseline = 0  
theta = 0     
factor_ron_roff = 2    
tau_PC = 250
ron_PC = 1./(tau_PC*(1+factor_ron_roff))
roff_PC = factor_ron_roff*ron_PC
mean_firing_rate_PC = (0.1)/1000  
duration_PC = 2000 
tau_IN = 50               
ron_IN = 1./(tau_IN*(1+factor_ron_roff))
roff_IN = factor_ron_roff*ron_IN
mean_firing_rate_IN = (0.5)/1000
duration_IN = 2000 
sampling_rate = 5      
dt = 1/sampling_rate 
qon_qoff_type = 'balanced'
Er_exc, Er_inh = (0, -75)
target = 12
on_off_ratio = 1.5

# Initiate Pyramidal cell models
PC_i = 35
current_PC = Barrel_PC('current', dt=dt)
dynamic_PC = Barrel_PC('dynamic', dt=dt)
current_PC.store()
dynamic_PC.store()

# Create results DataFrame
vars_to_track = ['input_theory', 'dynamic_theory', 'hidden_state',
                 'inj_current', 'current_volt', 'current_spikes',
                 'inj_dynamic', 'dynamic_volt', 'dynamic_spikes']
results_PC = pd.DataFrame(columns=vars_to_track)

# Pyramidal Cell simulation
succesful_runs = 0
while succesful_runs < 10:
    # Make input theory and hidden state for Pyramidal Cell
    [input_theory, dynamic_theory, hidden_state] = make_dynamic_experiments(qon_qoff_type, baseline, tau_PC, factor_ron_roff, mean_firing_rate_PC, sampling_rate, duration_PC)

    # Scale input and Check
    inj_current = scale_to_freq(current_PC, input_theory, target, on_off_ratio, 'current', duration_PC, hidden_state, dt, PC_i)
    if inj_current == False:
        continue
    inj_dynamic = scale_to_freq(dynamic_PC, dynamic_theory, target, on_off_ratio, 'dynamic', duration_PC, hidden_state, dt, PC_i)
    if inj_dynamic == False:
        continue
        
    # Run Pyramidal Cell
    current_PC.restore()
    dynamic_PC.restore()
    current_PC_M, current_PC_S = current_PC.run(inj_current, duration_PC, PC_i)
    dynamic_PC_M, dynamic_PC_S = dynamic_PC.run(inj_dynamic, duration_PC, PC_i)

    # Store results       
    data = np.array([input_theory, dynamic_theory, hidden_state,
                    current_PC_M.I_inj[0]/uA, current_PC_M.v[0]/mV, current_PC_S.t/ms,
                    dynamic_PC_M.I_inj[0]/uA, dynamic_PC_M.v[0]/mV, dynamic_PC_S.t/ms], dtype=list)
    data = pd.DataFrame(data=data, index=vars_to_track).T
    results_PC = results_PC.append(data, ignore_index=True)

    # Keep count
    succesful_runs += 1

# Keep it clean
try:
    clear_cache('cython')
except:
    pass

# Initiate Interneuron models
IN_i = 11
current_IN = Barrel_IN('current', dt=dt)
dynamic_IN = Barrel_PC('dynamic', dt=dt)
current_IN.store()
dynamic_IN.store()

# Create results DataFrame
results_IN = pd.DataFrame(columns=vars_to_track)

# Interneuron simulation
succesful_runs = 0
while succesful_runs < 10:
    # Make iput theory and hidden state for interneurons
    [input_theory, dynamic_theory, hidden_state] = make_dynamic_experiments(qon_qoff_type, baseline, tau_IN, factor_ron_roff, mean_firing_rate_IN, sampling_rate, duration_IN)

    # Scale input and check
    inj_current = scale_to_freq(current_IN, input_theory, target, on_off_ratio, 'current', duration_IN, hidden_state, dt, IN_i)
    if inj_current == False:
        continue
    inj_dynamic = scale_to_freq(dynamic_IN, dynamic_theory, target, on_off_ratio, 'dynamic', duration_IN, hidden_state, dt, IN_i)
    if inj_dynamic == False: 
        continue

    # Run Interneurons 
    current_IN.restore()
    dynamic_IN.restore()
    current_IN_M, current_IN_S = current_IN.run(inj_current, duration_IN, IN_i)
    dynamic_IN_M, dynamic_IN_S = dynamic_IN.run(inj_dynamic, duration_IN, IN_i)

    # Store results       
    data = np.array([input_theory, dynamic_theory, hidden_state,
                    current_IN_M.I_inj[0]/uA, current_IN_M.v[0]/mV, current_IN_S.t/ms,
                    dynamic_IN_M.I_inj[0]/uA, dynamic_IN_M.v[0]/mV, dynamic_IN_S.t/ms], dtype=list)
    data = pd.DataFrame(data=data, index=vars_to_track).T
    results_IN = results_IN.append(data, ignore_index=True)

    # Keep count
    succesful_runs += 1

# Save data
results_PC.to_pickle('results/results_PC.pkl')
results_IN.to_pickle('results/results_IN.pkl')

# Clean cache
try:
    clear_cache('cython')
except:
    pass
