# -*- coding: utf-8 -*-
"""
Preprocessing of PCG data.

@author: Agnieszka Kaczmarczyk
"""

import numpy as np
import wave_operations

def decimate(signal, params, f_k):
    f_p = params[2]
    n = (int)(f_p / f_k)
    signal_len = (int)(params[3] / n)
    
    signal_out = np.zeros(signal_len)
    
    for index in range(0, signal_len):
        signal_out[index] = signal[index * n]
        
    return signal_out
    
def normalize(signal):
    return signal * 1.0 / max(abs(signal))
