# -*- coding: utf-8 -*-
"""
Script for PCG signal segmentation. Segmentation based on S-Transform, source: 
"A robust heart sounds segmentation module based on S-transform.", A.Moukadem, 
A.Dieterlen, N.Hueber, C.Brandt.

@author: Agnieszka Kaczmarczyk
"""

import numpy as np
import wave_operations as wo
import preprocessing as pr
import math
import cmath

f = 2000

def calculate_S_transform(signal):
    signal_len = len(signal)
    S = np.zeros((signal_len, signal_len), dtype = 'complex')
    
    for tau_frame in range(0, signal_len):
        for t_frame in range(0, signal_len):
            S[tau_frame][t_frame] = (signal[t_frame] * (calculate_window(signal, ((tau_frame - t_frame)*1.0/f))) * cmath.exp((-2j) * math.pi * f * (t_frame / f)))
        print tau_frame
    return S
    
def calculate_window(signal, t):
    return (f / math.sqrt(2 * math.pi)) * math.exp(((-t**2) * (f**2)) / 2)
    
def calculate_SSE(S):
    signal_len = len(S)
    SSE = np.zeros(signal_len)
    for tau_frame in range(0, signal_len):
        for t_frame in range(0, signal_len):
            k1 = (abs(S[tau_frame][t_frame]))**2
            k2 = 0
            if (k1 != 0):
                k2 = cmath.log10(k1)
            SSE[tau_frame] = SSE[tau_frame] + (k1 * k2)
    return SSE
