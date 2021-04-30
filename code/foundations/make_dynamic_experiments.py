'''
    make_dynamic_experiments.py

    Make LUT of a dynamic input current based on a artificial network responding to a hidden state
    The method is described in the following paper:
    Zeldenrust, F., de Knecht, S., Wadman, W. J., Denève, S., Gutkin, B., Knecht, S. De, Denève, S. (2017). 
    Estimating the Information Extracted by a Single Spiking Neuron from a Continuous Input Time Series. 
    Frontiers in Computational Neuroscience, 11(June), 49. doi:10.3389/FNCOM.2017.00049
    Please cite this reference when using this method.
    
    NB Make sure that you save the hidden state with the experiments, it is
    essential for the information calculation!
'''
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import numpy as np
import matplotlib.pyplot as plt
from foundations.dynamic_clamp import get_g0
from foundations.input import Input

def make_dynamic_experiments(qon_qoff_type, baseline, tau, factor_ron_roff, mean_firing_rate, sampling_rate, duration, seed=None):
    ''' Make input current look up table (LUT) based on a artificial network responding
        to a hidden state.

    INPUT:
        qon_qoff_type (str): The method of qon/qoff generation. Options are normal,
                             balanced and balanced_uniform.
        baseline (pA): Baseline for scaling the input current in picoampere.
        amplitude_scaling (pA): Scaling of the stimulus in picoampere
        tau (ms): Switching speed of the hidden state in milliseconds.
        mean_firing_rate (kHz): Mean firing rate of the artificial neurons in kilohertz.
        sampling rate (kHZ): Sampling rate of the experimental setup (injected current) 
                             in kilohertz.
        duration (ms): Length of the duration in milliseconds.
        dv (float): resolution of voltage steps  
        seed (optional): Seed used in the random number generator.

    OUTPUT: 
        exc_LUT(dict): dictionary of the injected current per voltage.
        inh_LUT(dict): dictionary of the injected current per voltage.
        hidden_state: 1xN array with hidden state values 0=off 1=on.
    '''
    # Set RNG seed, if no seed is provided
    if seed == None:
        np.random.seed()
        seed = np.random.randint(1000000000)

    # Fixed parameters
    N = 1000                            
    dt = 1./sampling_rate
    tau_exponential_kernel = 5 
    alpha = np.sqrt(1/8)            # SEM * N
    stdq = alpha*mean_firing_rate
    ron = 1./(tau*(1+factor_ron_roff))
    roff = factor_ron_roff*ron
    v_rest = -65
    Er_exc, Er_inh = (0, -75)

    #Create input from artifical network
    input_bayes = Input()
    input_bayes.dt = dt
    input_bayes.T = duration
    input_bayes.kernel = 'exponential'
    input_bayes.kerneltau = tau_exponential_kernel
    input_bayes.ron = ron
    input_bayes.roff = roff
    input_bayes.seed = seed
    input_bayes.xseed = seed

    # Create qon/qoff
    if qon_qoff_type == 'normal':
        mutheta = 1             #The summed difference between qon and qoff
        alphan = alpha
        regime = 1
        [input_bayes.qon, input_bayes.qoff] = input_bayes.create_qonqoff(mutheta, N, alphan, regime, seed)
    elif qon_qoff_type == 'balanced':
        [input_bayes.qon, input_bayes.qoff] = input_bayes.create_qonqoff_balanced(N, mean_firing_rate, stdq, seed)
    elif qon_qoff_type == 'balanced_uniform':
        minq = 10                  
        maxq = 100
        [input_bayes.qon, input_bayes.qoff] = input_bayes.create_qonqoff_balanced_uniform(N, minq, maxq, seed)
    else: 
        raise SyntaxError('No qon/qoff creation type specified')
    
    #Generate weights and hiddenstate
    input_bayes.get_all()
    input_bayes.x = input_bayes.markov_hiddenstate()

    #Generate exc and inh
    g0_exc, g0_inh = get_g0(v_rest, input_bayes.w, Er_exc, Er_inh)
    g_exc = input_bayes.markov_input(g0_exc)
    g_inh = input_bayes.markov_input(g0_inh)
    dynamic_theory = (g_exc, g_inh)

    #Generate input_current for comparison
    input_theory = input_bayes.markov_input()
   
    # #SanityCheck for input (Vm=-40) and hiddenstate
    # fig, axs = plt.subplots(2, figsize=(12,12))
    # fig.suptitle('Dynamic Clamp conductances')

    # for idx, val in enumerate(input_bayes.x):
    #     if val == 1:
    #         axs[0].axvline(idx, c='lightgray')
    #         axs[1].axvline(idx, c='lightgray')

    # axs[0].plot(g_exc, c='red')
    # axs[0].set(ylabel='Exc. conductance [mS]')

    # axs[1].plot(g_inh, c='blue')
    # axs[1].set(ylabel='Inh. conductance [mS]')
    
    # plt.show()

    return [input_theory, dynamic_theory, input_bayes.x]
