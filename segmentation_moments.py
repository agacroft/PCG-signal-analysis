# -*- coding: utf-8 -*-
"""
Script for PCG signal segmentation. Segmantation based on "The moment 
segmentation analysis of heart sound pattern" by Z.Yan, Z.Yiang, A.Miyamoto,
Y.Wei

@author: Agnieszka Kaczmarczyk
"""

delta = 0.05
l = 0.5

import numpy as np

def prepare_scale_parameters (freq):
    Fs = freq    
    delta = 0.05 * Fs
    l = 0.5 * Fs
    delta = 0.05    # [s]
    l = 0.5         # [s]
    
    return delta, l
    
def calculate_c(signal, freq):
    start_frame = (int)(l * freq)
    stop_frame = len(signal) - start_frame
    delta_frame = (int)(delta * freq)

    c = np.zeros(len(signal))
    
    for t in range(start_frame, stop_frame):

        y_dash_tau = sum(signal[t - delta_frame : t + delta_frame])
        y_dash_tau = y_dash_tau * (1 / (2 * delta))
        
        for tau in range(t - delta_frame, t + delta_frame):
            c[t] = c[t] + (signal[tau] - y_dash_tau)**2
            
    return c

def calculate_I(c, freq):
    start_frame = (int)(l * freq)
    stop_frame = len(c) - start_frame
    delta_frame = (int)(l * freq)
    
    I_moment = np.zeros(len(c)) 
    
    for t in range(start_frame, stop_frame):
        
        for tau in range(t - delta_frame, t + delta_frame):
            I_moment[t] = I_moment[t] + ((tau**2) * c[tau]) - (2 * t * tau * c[tau]) + ((t**2) * c[tau])
            
    return I_moment
    
def calculate_mi(c, I_moment, freq):
    start_frame = (int)(l * freq)
    stop_frame = len(c) - start_frame
    delta_frame = (int)(l * freq)
    
    mi = np.zeros(len(c))    
    
    for t in range(start_frame, stop_frame):
        
        nominator = 0
        denominator = 0
        for tau in range(t - delta_frame, t + delta_frame):
            nominator = nominator + (((tau - t)**2) * c[tau])
            denominator = denominator + c[tau]
        mi[t] = nominator / denominator
        
    return mi
    
def calculate_I_mi_t_dash(c, freq):
    start_frame = (int)((l+delta) * freq)
    stop_frame = len(c) - start_frame
    delta_l_frame = (int)(l * freq)
    delta_frame = (int)(delta * freq)
    
    I_t_dash = np.zeros(len(c))  
    mi_t_dash = np.zeros(len(c))     
    
    for t in range(start_frame, stop_frame):
    
        denominator = 0
        for tau in range(t - delta_frame, t + delta_frame):
            denominator = denominator + c[tau]
        
        for tau in range(t - delta_l_frame, t + delta_l_frame):
            I_t_dash[t] = I_t_dash[t] + (((tau/freq - calculate_t_dash(c, tau, freq))**2) * c[tau])   
            
        mi_t_dash[t] = I_t_dash[t] / denominator
    
    return I_t_dash, mi_t_dash
    
def calculate_t_dash(c, t, freq):
    nominator = 0
    denominator = 0
    delta_frame = (int)(delta * freq)
    
    for tau in range(t - delta_frame, t + delta_frame):
        nominator = nominator + tau/freq * c[tau]
        denominator = denominator + c[tau]
    t_dash = nominator / denominator
    
    return t_dash
        
def calculate_S(signal, t, k):
    S = 0
    T = np.arange(0, t)
    for tau in T:
        S = S + ((signal[tau])**k)
        
    return S
    
def calculate_delta_S(signal, freq, t, k):
    delta_frame = (int)(delta * freq)

    return calculate_S(signal, (t + delta_frame), k) - calculate_S(signal, (t - delta_frame), k)
    
def calculate_J(signal, freq, t, k):
    J = 0
    delta_frame = (int)(delta * freq)
    
    for tau in range(t - delta_frame, t + delta_frame):
        J = J + (((tau/freq)**k) * calculate_delta_S(signal, freq, tau, k))
        
    return J / (2 * delta)
    
def calculate_delta_J(signal, freq, t, k):
    delta_frame = (int)(l * freq)

    return calculate_J(signal, freq, (t + delta_frame), k) - calculate_J(signal, freq, (t - delta_frame), k)
    
def calculate_I_moment_mi_2(signal, freq):
    start_frame = (int)(2 * l * freq)
    stop_frame = len(signal) - start_frame

    I_moment_2 = np.zeros(len(signal))
    mi_2 = np.zeros(len(signal))
    
    for t in range(start_frame, stop_frame):
        I_moment_2[t] = (calculate_delta_J(signal, freq, t, 2)) - (2 * calculate_delta_J(signal, freq, t, 1) * (t/freq)) + (calculate_delta_J(signal, freq, t, 0) * ((t/freq)**2))  
        mi_2[t] = I_moment_2[t] / (calculate_delta_J(signal, freq, t, 0) * (t/freq))
    
    return I_moment_2, mi_2
    