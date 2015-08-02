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
import s12_determinator as s12
from parametrization import Parameters
import murmurs_detector as mur
import os
from os import listdir
from os.path import isfile, join

plt.close('all')
freq = 4000

my_path = os.getcwd() + '\\test'
wave_files = [ f for f in listdir(my_path) if isfile(join(my_path,f)) ]

for wave_file in wave_files[:]:
    wave_file_path = my_path + '\\' + wave_file
    print wave_file_path
    signal_PCG, params = wo.read_wavefile(wave_file_path)
				
    # Preprocessing of the signal: removing beginnings and endings of signal.
    signal_PCG = signal_PCG[(int(params[2] * 0.3)) : (len(signal_PCG) - int(params[2] * 0.3))]
    # Preprocessing of the signal: filtering.
    cutoff = 195
    signal_PCG = pr.butter_lowpass_filter(signal_PCG, cutoff, freq, 1)
    # Preprocessing of the signal: decimation.
    signal_PCG = pr.decimate(signal_PCG, params, freq)
				
    # Prepare signal for STFT transformations.
    signal_to_stft = np.copy(signal_PCG)

    # Preprocessing of the signal: normalization.
    signal_PCG = pr.normalize(signal_PCG)
    
    signal_PCG_original = np.copy(signal_PCG)
    
    # Denoising histogram using histogram method.
    signal_PCG = segm.histogram_denoising(signal_PCG)
    
    # Determine heart rate.
    heart_rate = segm.heart_rate(signal_PCG, freq) 
    print heart_rate

    # Shannon energy envelope.
    shannon_envelope = segm.envelope(signal_PCG, freq)
    
    # Thresholding to find S1, S2 peaks.
#    thr, starts, stops, heart_rate, peaks_energy = threshold.determine_threshold(shannon_envelope, freq, heart_rate)
    thr, starts, stops, heart_rate, peaks_energy, signal_type = threshold.threshold_with_custom_threshold(shannon_envelope, freq, heart_rate, 0.15)
    print signal_type
    # Finding boundaries between cycles.
    boundaries = s12.find_cycle_start(signal_PCG, starts, heart_rate, freq) 

    # S1 & S2 peaks searching.
#    peaks_max, peaks_sc = s12.peaks_fft_parameters(signal_PCG_original, starts, stops, freq)
    s1 = []    
    s2 = []
    s = []
    if signal_type == 1:
        s1, s2, s = s12.determine_s12_with_type_1(signal_PCG_original, starts, stops, boundaries, peaks_energy, heart_rate, freq)
    
    elif signal_type == 2:
        s1 = s12.determine_s1_with_type_2(starts, stops, boundaries, peaks_energy, heart_rate, freq)
        
    # Check murmur candidates time with peaks time.
    murmur_candidates_t = mur.murmurs(signal_to_stft, freq, starts, stops, s1, s2, s, heart_rate)

    # Parametrization of signal.        
    parameters = Parameters(signal_PCG_original, freq, heart_rate, s1, s2, s, starts, stops, signal_type)   
    t1 = parameters.t1()
    t2 = parameters.t2()
    t12 = parameters.t12()
    t21 = parameters.t21()
    total_power_systole = parameters.total_power_systole()
    mean12 = parameters.mean12()
    sc1 = parameters.s1_fft()
    sc2 = parameters.s2_fft()
    tones_std = parameters.t_variance()
    tones_mean, tones_mean_p = parameters.tones_mean()
    breaks, percentage = parameters.breaks_power()
    breaks_sc = parameters.breaks_fft()
        
    print 't1: ' + str(t1)
    print 't2: ' + str(t2)
    print 't12: ' + str(t12)
    print 't21: ' + str(t21)
    print 'total_power_systole: ' + str(total_power_systole)
    print 'mean12: ' + str(mean12)
    print 'sc1: ' + str(sc1)
    print 'sc2: ' + str(sc2)
    print 'tones std: ' + str(tones_std)
    print 'tones mean: ' + str(tones_mean) + ' ' + str(tones_mean_p)
    print 'breaks: ' + str(breaks) + ' ' + str(percentage)
    print 'breaks_sc: ' + str(breaks_sc)
        
#     Plotting results: original signal with visualized cycles boundaries and 
#     tones; signal after histogram cleaning; Shannon Energy Envelope  
    T = 1.0/freq
    length = len(signal_PCG)
    t = np.arange(0, length, 1)
    t = t * T
    f, axarr = plt.subplots(3, sharex=True)
    axarr[1].plot(t, signal_PCG)
    axarr[0].plot(t, signal_PCG_original)
    axarr[0].set_title(wave_file + ' ' + str(heart_rate))
    for boundary in boundaries:
        axarr[0].axvline(boundary * 1.0/ freq, color = 'red') 
    for index in s1:
        axarr[0].axvline(starts[index] * 1.0/ freq, color = 'green')
        axarr[0].axvline(stops[index] * 1.0/ freq, color = 'green')
    for index in s2:
        axarr[0].axvline(starts[index] * 1.0/ freq, color = 'yellow')
        axarr[0].axvline(stops[index] * 1.0/ freq, color = 'yellow')
    for index in s:
        axarr[0].axvline(starts[index] * 1.0/ freq, color = 'magenta')
        axarr[0].axvline(stops[index] * 1.0/ freq, color = 'magenta')
    axarr[2].plot(t, shannon_envelope)
    axarr[2].axhline(y=thr, xmin=0, xmax=1, c="red",linewidth=0.5,zorder=0)

#    plt.savefig('plots\\' + wave_file[0:len(wave_file) - 4] + '.png')
#    plt.close()
