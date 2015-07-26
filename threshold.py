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
threshold_start = 0.05
threshold_stop = 0.7

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
        
            wo.plot_wave_signal(signal, freq)
            plt.axhline(y = threshold, xmin = 0, xmax = 3, c = "red", linewidth = 0.5, zorder = 0)
        
            break 
        elif ((2 - rate_confidence) * heart_rate <= rate and (2 + rate_confidence) * heart_rate >= rate):
            heart_rate = 2 * heart_rate
            print str(threshold) + ' - HERE!'
            thr = threshold
        
            wo.plot_wave_signal(signal, freq)
            plt.axhline(y = threshold, xmin = 0, xmax = 3, c = "red", linewidth = 0.5, zorder = 0)
        
            break 
        
    return thr, begginings, endings, heart_rate
    
# Check if signal doesn't start or stop while being inside the peak.
def investigate_tone_boundaries(begginings, endings):
    start = np.copy(begginings)
    stop = np.copy(endings)
    if start[0] > stop[0]:
        stop = stop[1:]
    
    if len(start) > len(stop):
        start = start[0:len(start) - 1]
        
    return start, stop