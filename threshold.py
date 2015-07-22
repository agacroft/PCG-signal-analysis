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

def determine_threshold(signal, freq):    
    
    signal = pr.normalize(signal)
    is_above = False
    i = 0
    
    thresholds = np.arange(0.1, 0.8, 0.05)
    
    for threshold in thresholds:
        under = 0
        begginings = []
        endings = []
        i = 0
        for x in signal:
            if x < threshold:
                under = under + 1
                if is_above == True:
                    is_above = False
                    begginings.append(i)
                    # dodac poczatek tonu
            else:
                if is_above == False:
                    is_above = True
                    endings.append(i)
            i = i + 1
                    # dodac koniec tonu
        n = len(begginings)
        rate = n / (len(signal) * 1.0/ freq) * 30
        # strzelac w freq = 140
        print str(threshold) + ': ' + str(under * 1.0 / len(signal)) + ' ' + str(n) + ' ' + str(rate)
        
        wo.plot_wave_signal(signal, freq)
        plt.axhline(y = threshold, xmin = 0, xmax = 3, c = "red", linewidth = 0.5, zorder = 0)