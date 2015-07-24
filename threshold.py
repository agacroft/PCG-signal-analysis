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

threshold_step = 0.1
threshold_start = 0.1
threshold_stop = 0.8

def determine_threshold(signal, freq):    
    
    signal = pr.normalize(signal)
    i = 0
    
    thresholds = np.arange(threshold_start, threshold_stop, threshold_step)
    
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
                    begginings.append(i)
            else:
                if is_above == False:
                    is_above = True
                    if len(begginings) > 0:
                        endings.append(i)
            i = i + 1
        begginings, endings = investigate_tone_boundaries(begginings, endings)
        n = len(begginings)
        rate = n / (len(signal) * 1.0/ freq) * 30
        
        print str(threshold) + ': ' + str(under * 1.0 / len(signal)) + ' ' + str(n) + ' ' + str(rate)    
        
#        wo.plot_wave_signal(signal, freq)
#        plt.axhline(y = threshold, xmin = 0, xmax = 3, c = "red", linewidth = 0.5, zorder = 0)
        
def investigate_tone_boundaries(start, stop):
    if len(start) > len(stop):
        start = np.delete(start, len(start) - 1)
        
    return start, stop