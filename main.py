# -*- coding: utf-8 -*-
"""
Main.

@author: Agnieszka Kaczmarczyk
"""

import matplotlib.pyplot as plt
import numpy as np
import wave_operations as wo
import preprocessing as pr
import segmentation as segm
import threshold
import os
from os import listdir
from os.path import isfile, join

plt.close('all')
freq = 4000

my_path = os.getcwd() + '\\normal signals'
wave_files = [ f for f in listdir(my_path) if isfile(join(my_path,f)) ]

for wave_file in wave_files[0:20]:
    wave_file_path = my_path + '\\' + wave_file
    print wave_file_path
    signal_PCG, params = wo.read_wavefile(wave_file_path)
    # Preprocessing of the signal: decimation.
    signal_PCG = pr.decimate(signal_PCG, params, freq)
    
    # Preprocessing of the signal: normalization.
    signal_PCG = pr.normalize(signal_PCG)
    
    # Preprocessing of the signal: filtering.
    cutoff = 100
    signal_PCG = pr.butter_lowpass_filter(signal_PCG, cutoff, freq, 1)
    
    signal_PCG2 = segm.histogram_denoising(signal_PCG)
    
    heart_rate = segm.heart_rate(signal_PCG, freq)
    heart_rate2 = segm.heart_rate(signal_PCG2, freq) 

    # Shannon energy envelope
    shannon_envelope = segm.envelope(signal_PCG, freq)
    shannon_envelope2 = segm.envelope(signal_PCG2, freq)
    
    threshold.determine_threshold(shannon_envelope, freq)
    threshold.determine_threshold(shannon_envelope2, freq)
    
    T = 1.0/freq
    length = len(signal_PCG)
    t = np.arange(0, length, 1)
    t = t * T
    f, axarr = plt.subplots(3, sharex=True)
    axarr[0].plot(t, signal_PCG)
    axarr[0].set_title(wave_file)
    axarr[1].plot(t, shannon_envelope)
    axarr[2].plot(t, shannon_envelope2)
