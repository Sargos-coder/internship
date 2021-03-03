''' helpers.py
    
    Helps you out :)
''' 
import numpy as np
from brian2 import *

def scale_input_theory(input_theory, baseline, amplitude_scaling, dt):
    ''' docstring
    '''
    scaled_input = (baseline + input_theory * amplitude_scaling)*namp
    inject_input = TimedArray(scaled_input, dt=dt*ms)
    return inject_input

def scale_dynamic_input(exc_LUT, inh_LUT, Er_exc, Er_inh, scale_exc_inh, dt):
    ''' docstring
    '''
    g_exc = abs(exc_LUT[-65] / (-65 - Er_exc))*mS * scale_exc_inh
    g_inh = abs(inh_LUT[-65] / (-65 - Er_inh))*mS * scale_exc_inh
    g_exc = TimedArray(g_exc, dt=dt*ms)
    g_inh = TimedArray(g_inh, dt=dt*ms)
    return (g_exc, g_inh)

def make_spiketrain(S, hiddenstate, dt):
    ''' docstring
    '''
    spiketrain = np.zeros((1, hiddenstate.shape[0]))
    spikeidx = np.array(S.t/ms/dt, dtype=int)
    spiketrain[:, spikeidx] = 1
    return spiketrain