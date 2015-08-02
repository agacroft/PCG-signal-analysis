# -*- coding: utf-8 -*-
"""
Preprocessing of PCG data.

@author: Agnieszka Kaczmarczyk
"""

import numpy as np
import wave_operations as wo
from scipy.signal import butter, lfilter
import scipy.fftpack
import matplotlib.pyplot as plt

def decimate(signal_in, params, f_k):
    f_p = params[2]
    n = (int)(f_p / f_k)
    signal_len = (int)(len(signal_in) / n)
    
    signal_out = np.zeros(signal_len)
    
    for index in range(0, signal_len):
        signal_out[index] = signal_in[index * n]
        
    return signal_out
    
def normalize(signal_in):
    return signal_in * 1.0 / max(abs(signal_in))

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=1):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_bandpass(lowcut, highcut, fs, order=1):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
 
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def show_fft(signal_in, params):
    FFT = abs(scipy.fft(signal_in[0: params[2] - 1], params[2]))
    freq = scipy.fftpack.fftfreq(params[3], 1.0/params[2])

    plt.plot(freq[0: params[2]/2], abs(FFT[0: params[2]/2]))

def spectral_centroid(FFT, frequencies):
        spectral_centroid_nominator = 0
        spectral_centroid_denominator = 0
        for index in range(0, len(FFT)):
            spectral_centroid_nominator = spectral_centroid_nominator + (frequencies[index] * FFT[index])
            spectral_centroid_denominator = spectral_centroid_denominator + FFT[index]
            
        return spectral_centroid_nominator / spectral_centroid_denominator

def fft_freq(signal_in, freq):
    FFT = abs(scipy.fft(signal_in))
    frequencies = scipy.fftpack.fftfreq(len(signal_in), 1.0 / freq)
				
#    plt.figure()
#    plt.plot(frequencies[0: len(FFT)/2], FFT[0: len(FFT)/2])

    return FFT, frequencies