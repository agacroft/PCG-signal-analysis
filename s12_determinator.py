# -*- coding: utf-8 -*-
"""
Script for determining S1 and S2 peaks.

@author: Agnieszka Kaczmarczyk
"""

import numpy as np

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
    
def determine_s12(starts, stops, boundaries):
    ranges_n = len(boundaries) - 1
    peaks_n = len(starts)
    peaks_lengths = [b - a for a,b in zip(starts, stops)]
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
            s1_index = np.argmax(peaks_lengths[start_index : stop_index + 1], axis = 0) + start_index        
            s1.append(s1_index)
            peaks_lengths[s1_index] = 0
            s2_index = np.argmax(peaks_lengths[start_index : stop_index + 1], axis = 0) + start_index     
            s2.append(s2_index)
            peaks_lengths[s2_index] = 0
        
    return s1, s2