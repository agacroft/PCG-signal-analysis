# -*- coding: utf-8 -*-
"""
Segmentation based on Shannon Energy.

@author: Agnieszka Kaczmarczyk
"""

import preprocessing as pr
import wave_operations as wo
import numpy as np

def energy(signal_in):
    return [x**2 for x in signal_in]

def shannon_entrophy(signal_in):
    return [(-abs(x) * (logarithm(x))) for x in signal_in]
    
def shannon_energy(signal_in):
    return [((-(x**2)) * (logarithm(x**2))) for x in signal_in]    
    
def logarithm(x):
    if x == 0:
        return 0
    else:
        return np.log10(x)
        
def moving_average(signal_in, n = 100) :
    mov_av = np.zeros(len(signal_in))
    mov_av[0:n - 1] = signal_in[0:n - 1]
    for t in range(n - 1, len(mov_av)):
        mov_av[t] = np.average(signal_in[t - n + 1 : t])
    return mov_av

def shannon_energy_i(x):
    return ((-(x**2)) * (logarithm(x**2)))
    
def shannon_energy_envelope(signal_in, freq):
    shannon_envelope = np.zeros(len(signal_in))
    delta_t = 0.01
    delta_t_frame = int(delta_t * freq)
    N = 2 * delta_t_frame + 1
    
    for x in range (delta_t_frame, (len(shannon_envelope) - delta_t_frame)):
        for tau in range(x - delta_t_frame, x + delta_t_frame):
            shannon_envelope[x] = shannon_envelope[x] + shannon_energy_i(signal_in[tau])
        shannon_envelope[x] = shannon_envelope[x] / N
        
    return shannon_envelope

def normalize_shannon(shannon_energy):
    m = np.average(shannon_energy)
    std = np.std(shannon_energy)
    return [((x - m)/ std) for x in shannon_energy]
