# -*- coding: utf-8 -*-
"""
Script for basic operations on wave files. 

@author: Agnieszka Kaczmarczyk
"""

import wave
import matplotlib.pyplot as plt
import numpy as np

def read_wavefile(path):
    wave_data = wave.open(path, 'r')
    
    frames = wave_data.readframes(-1)
    frames = np.fromstring(frames, 'Int16')
    
    params = wave_data.getparams()
    
    return frames, params


def plot_wave_signal(signal, params):
    Fs = params[2]
    T = 1.0/Fs
    length = len(signal)
    t = np.arange(0, length, 1)
    t = t * T
    
    plt.figure()
    plt.title('PCG signal')
    plt.plot(t, signal)
    
    
filepath = '201101070538.wav'
signal, params = read_wavefile(filepath)
plot_wave_signal(signal, params)