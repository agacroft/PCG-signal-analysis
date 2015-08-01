# -*- coding: utf-8 -*-
"""
Script for determining threshold for segmentation based on Shannon Energy 
envelope method.

@author: Agnieszka Kaczmarczyk
"""

import preprocessing as pr
import wave_operations as wo
import matplotlib.pyplot as plt
import numpy as np

threshold_step = 0.05
threshold_start = 0.1
threshold_stop = 0.7
rate_confidence = 0.21

def determine_threshold(signal, freq, heart_rate):    
    
    signal = pr.normalize(signal)
    i = 0
    
    thresholds = np.arange(threshold_start, threshold_stop, threshold_step)
    thr = 0
    begginings = []
    endings = []
    
    for threshold in thresholds:
        under = 0
        is_above = False
        begginings = []
        endings = []
        i = 0
        for x in signal:
            if x < threshold:
                under = under + 1
                if is_above == True:
                    is_above = False
                    endings.append(i)
            else:
                if is_above == False:
                    is_above = True
                    begginings.append(i)
            i = i + 1
        begginings, endings = investigate_tone_boundaries(begginings, endings)
        n = len(begginings)
        rate = n / (len(signal) * 1.0/ freq) * 30
        
        print str(threshold) + ': ' + str(under * 1.0 / len(signal)) + ' ' + str(n) + ' ' + str(rate)    
          
        if ((1 - rate_confidence) * heart_rate <= rate and (1 + rate_confidence) * heart_rate >= rate):
            print str(threshold) + ' - HERE!'
            thr = threshold
        
#            wo.plot_wave_signal(signal, freq)
#            plt.axhline(y = threshold, xmin = 0, xmax = 3, c = "red", linewidth = 0.5, zorder = 0)
        
            break 
        elif ((2 - rate_confidence) * heart_rate <= rate and (2 + rate_confidence) * heart_rate >= rate):
            heart_rate = 2 * heart_rate
            print str(threshold) + ' - HERE!'
            thr = threshold
        
#            wo.plot_wave_signal(signal, freq)
#            plt.axhline(y = threshold, xmin = 0, xmax = 3, c = "red", linewidth = 0.5, zorder = 0)
        
            break 
        
    n = len(begginings)   
    peaks_energy = np.zeros(n)
    for index in range(0, n - 1):
        peaks_energy[index] = sum(signal[begginings[index] : endings[index]])
        
    return thr, begginings, endings, heart_rate, peaks_energy
    
# Check if signal doesn't start or stop while being inside the peak.
def investigate_tone_boundaries(begginings, endings):
    start = np.copy(begginings)
    stop = np.copy(endings)
    if start[0] > stop[0]:
        stop = stop[1:]
    
    if len(start) > len(stop):
        start = start[0:len(start) - 1]
        
    return start, stop

# Use custom threshold for determining heart rate and peaks.
def threshold_with_custom_threshold(signal, freq, heart_rate, threshold):    
    
    thr = max(signal) * threshold
    signal = pr.normalize(signal)
    i = 0
    signal_type = 0
    # 1 - s1 & s2
    # 2 - only s1

    begginings = []
    endings = []
    
    under = 0
    is_above = False
    begginings = []
    endings = []
    i = 0
    for x in signal:
        if x < threshold:
            under = under + 1
            if is_above == True:
                is_above = False
                if (i - begginings[len(begginings) - 1]) > (freq * 0.02):
                    endings.append(i)
                else:
                    del begginings[-1]
        else:
            if is_above == False:
                is_above = True
                begginings.append(i)
        i = i + 1
    begginings, endings = investigate_tone_boundaries(begginings, endings)
    n = len(begginings)
    rate = n / (len(signal) * 1.0/ freq) * 30
        
    print str(threshold) + ': ' + str(under * 1.0 / len(signal)) + ' ' + str(n) + ' ' + str(rate)    
          
    if ((1 - rate_confidence) * heart_rate <= rate and (1 + rate_confidence) * heart_rate >= rate):
        heart_rate = (heart_rate + rate) / 2
        signal_type = 1
    elif ((2 - rate_confidence) * heart_rate <= rate and (2 + rate_confidence) * heart_rate >= rate):
        heart_rate = (2 * heart_rate + rate) / 2
        signal_type = 1
    elif ((1 - 3 * rate_confidence) * heart_rate <= rate and (1 - rate_confidence) * heart_rate >= rate):
        heart_rate = (heart_rate + 2 * rate) / 2
        signal_type = 2
    else:
        signal_type = 3
        
#            wo.plot_wave_signal(signal, freq)
#            plt.axhline(y = threshold, xmin = 0, xmax = 3, c = "red", linewidth = 0.5, zorder = 0)
        
    peaks_energy = np.zeros(n)
    for index in range(0, n - 1):
        peaks_energy[index] = sum(signal[begginings[index] : endings[index]])
        
    return thr, begginings, endings, heart_rate, peaks_energy, signal_type