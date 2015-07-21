# -*- coding: utf-8 -*-
"""
Script for PCG signal segmentation. Segmantation based on "The moment 
segmentation analysis of heart sound pattern" by Z.Yan, Z.Yiang, A.Miyamoto,
Y.Wei

@author: Agnieszka Kaczmarczyk
"""

delta = 0.02
l = 0.2

import wave_operations
import numpy as np

def prepare_scale_parameters (params):
    Fs = params[2]    
    delta = 0.05 * Fs
    l = 0.5 * Fs
    delta = 0.05    # [s]
    l = 0.5         # [s]
    
    return delta, l
    
def calculate_c(signal, params):
    start_frame = (int)(l * params[2])
    stop_frame = params[3] - start_frame
    delta_frame = (int)(delta * params[2])

    c = np.zeros(params[3])
    
    for t in range(start_frame, stop_frame):

        y_dash_tau = sum(signal[t - delta_frame : t + delta_frame])
        y_dash_tau = y_dash_tau * (1 / (2 * delta))
        
        for tau in range(t - delta_frame, t + delta_frame):
            c[t] = c[t] + (signal[tau] - y_dash_tau)**2
            
        print t
    return c

def calculate_I(c, params):
    start_frame = (int)(l * params[2])
    stop_frame = params[3] - start_frame
    delta_frame = (int)(l * params[2])
    
    I_moment = np.zeros(params[3]) 
    
    for t in range(start_frame, stop_frame):
        
        for tau in range(t - delta_frame, t + delta_frame):
            I_moment[t] = I_moment[t] + ((tau**2) * c[tau]) - (2 * t * tau * c[tau]) + ((t**2) * c[tau])
            
    return I_moment
    
def calculate_mi(c, I_moment, params):
    start_frame = (int)(l * params[2])
    stop_frame = params[3] - start_frame
    delta_frame = (int)(l * params[2])
    
    mi = np.zeros(params[3])    
    
    for t in range(start_frame, stop_frame):
        
        nominator = 0
        denominator = 0
        for tau in range(t - delta_frame, t + delta_frame):
            nominator = nominator + (((tau - t)**2) * c[tau])
            denominator = denominator + c[tau]
        mi[t] = nominator / denominator
        
    return mi
    
def calculate_I_mi_t_dash(c, params):
    start_frame = (int)(l * params[2])
    stop_frame = params[3] - start_frame
    delta_frame = (int)(l * params[2])
    
    I_t_dash = np.zeros(params[3])  
    mi_t_dash = np.zeros(params[3])     
    
    for t in range(start_frame, stop_frame):
        
        nominator = 0
        denominator = 0
        for tau in range(t - delta_frame, t + delta_frame):
            nominator = nominator + tau * c[tau]
            denominator = denominator + tau
        t_dash = nominator / denominator
        
        for tau in range(t - delta_frame, t + delta_frame):
            I_t_dash[t] = I_t_dash[t] + (((tau - t_dash)**2) * c[tau])   
            
        mi_t_dash[t] = I_t_dash[t] / denominator
    
    return I_t_dash, mi_t_dash
        
def calculate_S(signal, params, t, k):
    S = 0
    T = np.arange(0, t * params[2])
    for tau in T:
        S = S + ((signal[tau])**k)
        
    return S
    
def calculate_delta_S(signal, params, t, k):
    delta_frame = (int)(delta * params[2])

    return calculate_S(signal, params, (t + delta_frame), k) - calculate_S(signal, params, (t - delta_frame), k)
    
def calculate_J(signal, params, c, t, k):
    print 'J'
    print t
    print '\n'
    J = 0
    delta_frame = (int)(delta * params[2])
    
    for tau in range(t - delta_frame, t + delta_frame):
        J = J + ((tau**k) * c[tau])
        
    return J / (2 * delta)
    
def calculate_delta_J(signal, params, c, t, k):
    print 'delta J'
    print t
    print '\n'
    delta_frame = (int)(l * params[2])

    return calculate_J(signal, params, c, (t + delta_frame), k) - calculate_J(signal, params, c, (t - delta_frame), k)
    
def calculate_I_moment_mi_2(signal, params, c):
    start_frame = (int)(2 * l * params[2])
    stop_frame = params[3] - start_frame

    I_moment_2 = np.zeros(params[3])
    mi_2 = np.zeros(params[3])
    
    for t in range(start_frame, stop_frame):
        I_moment_2[t] = (calculate_delta_J(signal, params, c, t, 2)) - (2 * calculate_delta_J(signal, params, c, t, 1) * t) + (calculate_delta_J(signal, params, c, t, 0) * (t**2))
        mi_2[t] = I_moment_2[t] / (calculate_delta_J(signal, params, c, t, 0) * t)
    
    return I_moment_2, mi_2
    
