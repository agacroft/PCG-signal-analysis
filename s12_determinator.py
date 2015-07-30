# -*- coding: utf-8 -*-
"""
Script for determining S1 and S2 peaks.

@author: Agnieszka Kaczmarczyk
"""

import numpy as np
import preprocessing as pr
import matplotlib.pyplot as plt

def find_cycle_start(signal_in, starts, heart_rate, freq):
    cycle_frames = int(60.0 / heart_rate * freq)
    
    start_peak_frame = starts[0]
    
    start_cycle_time = int(start_peak_frame - (0.15 * cycle_frames))
    
    cycles_boundaries = []
    cycles_boundaries.append(start_cycle_time)
    new_boundary = 0    
    last_boundary = start_cycle_time
    signal_end = len(signal_in) 
    
    while new_boundary < signal_end:
        new_boundary = last_boundary + cycle_frames
        cycles_boundaries.append(new_boundary)
        last_boundary = new_boundary
        
    if cycles_boundaries[0] < 0:
        cycles_boundaries[0] = 0
    cycles_boundaries[len(cycles_boundaries) - 1] = signal_end - 1
    return cycles_boundaries
    
def determine_s12(starts, stops, boundaries, peaks_energy):
    ranges_n = len(boundaries) - 1
    peaks_n = len(starts)
    peaks_lengths = [b - a for a,b in zip(starts, stops)]
    peaks_weights = [0.3 * e + 0.7 * l for e,l in zip(peaks_energy, peaks_lengths)]    
    
    s1 = []
    s2 = []
    
    for range_index in range(0, ranges_n):
        range_start = boundaries[range_index]
        range_stop = boundaries[range_index + 1]
        
        start_index = -1
        stop_index = -1
        
        i = 0
        while start_index < 0 and i < peaks_n:
            if starts[i] > range_start:
                start_index = i
            else:
                i = i + 1
                
        i = 1 
        while stop_index < 0 and i < peaks_n:
            if stops[i] > range_stop and start_index < i:
                stop_index = i - 1
            else:
                i = i + 1
   
        if stop_index - start_index >= 1:
            s1_index = np.argmax(peaks_weights[start_index : stop_index + 1], axis = 0) + start_index        
            s1.append(s1_index)
            peaks_weights[s1_index] = 0
            s2_index = np.argmax(peaks_weights[start_index : stop_index + 1], axis = 0) + start_index     
            s2.append(s2_index)
            peaks_weights[s2_index] = 0
        
    return s1, s2
    
    
# Determining s1, s2 based also on type of signal.
def determine_s12_with_type_1(signal_original, starts, stops, boundaries, peaks_energy, heart_rate, freq):
    ranges_n = len(boundaries) - 1
    peaks_max, peaks_sc = peaks_fft_parameters(signal_original, starts, stops, freq)
    
    peaks_lengths = [b - a for a,b in zip(starts, stops)]
    peaks_weights2 = [0.3 * e + 0.7 * l for e,l in zip(peaks_energy, peaks_lengths)]    
    av_peaks_max = np.mean(peaks_max)
    av_peaks_sc = np.mean(peaks_sc)
    av_peaks_length = np.mean(peaks_lengths)
    for i in range(0, len(peaks_sc)):
        if peaks_sc[i] > 250:
            peaks_sc[i] = av_peaks_sc
    
    peaks_weights = [0.5 * ((av_peaks_sc - sc) / av_peaks_sc) + 0.5 * ((l - av_peaks_length) * 1.0 / av_peaks_length) for sc,l in zip(peaks_sc, peaks_lengths)]   
    
    for index in range(0, len(peaks_sc)):
        print str(index) + ' ' + str(peaks_lengths[index]) + ' ' + str(peaks_sc[index]) + ' ' + str(peaks_max[index]) + ' ' + str(peaks_weights[index]) + ' ' + str(peaks_weights2[index])
    
    starts_search = np.copy(starts)
    stops_search = np.copy(stops)    
    
    starts_search = np.append(starts_search, np.array([boundaries[len(boundaries) - 1] + int(0.1 * 60.0 / heart_rate * freq) + 2]))  
    stops_search = np.append(stops_search, np. array([boundaries[len(boundaries) - 1] + int(0.1 * 60.0 / heart_rate * freq) + 4]))
    
    peaks_n = len(starts_search)
    
    s1 = []
    s2 = []
    s12 = []
    for range_index in range(0, ranges_n):
        range_start = boundaries[range_index] - int(0.1 * 60.0 / heart_rate * freq)
        range_stop = boundaries[range_index + 1] + int(0.1 * 60.0 / heart_rate * freq)
        # Finding indexes of peaks in one cycle.
        start_index = -1
        stop_index = -1
        
        i = 0
        while start_index < 0 and i < peaks_n:
            if starts_search[i] > range_start:
                start_index = i
            else:
                i = i + 1
                
        i = 1 
        while stop_index < 0 and i < peaks_n:
            if stops_search[i] > range_stop and start_index < i:
                stop_index = i - 1
            else:
                i = i + 1
   
        if stop_index - start_index >= 1:
            s1_index = np.argmax(peaks_weights[start_index : stop_index + 1], axis = 0) + start_index  
            s1.append(s1_index)
            peaks_weights[s1_index] = -2
            s2_index = np.argmax(peaks_weights[start_index : stop_index + 1], axis = 0) + start_index           
            s2.append(s2_index)
            peaks_weights[s2_index] = -2
        elif start_index == stop_index and start_index > -1:
            s12.append(start_index)
            peaks_weights[start_index] = -2
        
    return s1, s2, s12
    
# Determining s1, s2 based also on type of signal.
def determine_s1_with_type_2(starts, stops, boundaries, peaks_energy, heart_rate, freq):
    ranges_n = len(boundaries) - 1
    
    peaks_lengths = [b - a for a,b in zip(starts, stops)]
    peaks_weights = [0.3 * e + 0.7 * l for e,l in zip(peaks_energy, peaks_lengths)]    
    
    starts_search = np.copy(starts)
    stops_search = np.copy(stops)    
    
    starts_search = np.append(starts_search, np.array([boundaries[len(boundaries) - 1] + int(0.1 * 60.0 / heart_rate * freq) + 2]))  
    stops_search = np.append(stops_search, np. array([boundaries[len(boundaries) - 1] + int(0.1 * 60.0 / heart_rate * freq) + 4]))
    
    peaks_n = len(starts_search)
    
    s1 = []
    
    for range_index in range(0, ranges_n):
        range_start = boundaries[range_index] - int(0.1 * 60.0 / heart_rate * freq)
        range_stop = boundaries[range_index + 1] + int(0.1 * 60.0 / heart_rate * freq)
        # Finding indexes of peaks in one cycle.
        start_index = -1
        stop_index = -1
        
        i = 0
        while start_index < 0 and i < peaks_n:
            if starts_search[i] > range_start:
                start_index = i
            else:
                i = i + 1
                
        i = 1 
        while stop_index < 0 and i < peaks_n:
            if stops_search[i] > range_stop and start_index < i:
                stop_index = i - 1
            else:
                i = i + 1
   
        if stop_index - start_index >= 0:
            s1_index = np.argmax(peaks_weights[start_index : stop_index + 1], axis = 0) + start_index        
            s1.append(s1_index)
            peaks_weights[s1_index] = 0
        
    return s1
    
def peaks_fft_parameters(signal, starts, stops, freq):
    n = len(starts)
    peaks_max_frequencies = []
    peaks_spectral_centroids = []
    for peak_index in range(0, n):
        peak_length_accuracy = int(0.1 * (stops[peak_index] - starts[peak_index]))
        peak_start = starts[peak_index] #+ peak_length_accuracy
        peak_stop = stops[peak_index]# + peak_length_accuracy
        FFT, frequencies = pr.fft_freq(signal[peak_start : peak_stop], freq)
        peaks_max_frequencies.append(max(FFT))
        peaks_spectral_centroids.append(pr.spectral_centroid(FFT[0: len(FFT)/2], frequencies[0: len(FFT)/2]))
        
#        plt.figure()
#        plt.plot(frequencies[0: len(FFT)/2], FFT[0: len(FFT)/2])
#        plt.title(str(peak_index))
    
    return peaks_max_frequencies, peaks_spectral_centroids