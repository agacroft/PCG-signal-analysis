# -*- coding: utf-8 -*-
"""
Script for PCG signal parametrization.
Used parameters:
- FFT for S1 - only plots as far
- FFT for S2 - only plots as far
- FFT for other peaks detected - not yet
- Wigner distribution of tones - not yet, not sure
- STFT on whole signal - not yet
- total power during systole (between end of S1 and start of S2)
- Q-factor during systole - not yet
- t1 - S1 durarion
- t2 - S2 duration
- t12 - time between end of S1 and start of S2
- t21 - time between end of S2 and start of next S1
- mean12 - maximum of means in regions between S1 - S2 and S2 - S1 - not yet

@author: Agnieszka Kaczmarczyk
"""

import numpy as np
import scipy
import matplotlib.pyplot as plt

class Parameters(object):
    def __init__(self, signal_PCG, freq, HR, S1, S2, peak_starts, peak_stops):
        self.signal = signal_PCG
        self.freq = freq
        self.heart_rate = HR
        self.s1 = S1
        self.s2 = S2
        self.peak_starts = peak_starts
        self.peak_stops = peak_stops
            
    def s1_fft(self):
        ffts = np.zeros((len(self.s1), len(self.signal)))

        plt.figure()
        for i in self.s1:
            signal_s1 = self.signal[self.peak_starts[i] : self.peak_stops[i]]
            FFT = abs(scipy.fft(signal_s1))
            frequencies = scipy.fftpack.fftfreq(len(signal_s1), 1.0 / self.freq)

            plt.plot(frequencies[0: self.freq/2], abs(FFT[0: self.freq/2]))
            plt.title(i)
            
    def s2_fft(self):
        ffts = np.zeros((len(self.s2), len(self.signal)))

        plt.figure()
        for i in self.s2:
            signal_s2 = self.signal[self.peak_starts[i] : self.peak_stops[i]]
            FFT = abs(scipy.fft(signal_s2))
            frequencies = scipy.fftpack.fftfreq(len(signal_s2), 1.0 / self.freq)
            
            plt.plot(frequencies[0: self.freq/2], abs(FFT[0: self.freq/2]))
            plt.title(i)
            
    def t1(self):
        t1s = np.zeros(len(self.s1))
        for i in self.s1:
            t1s[i] = (self.peak_stops[i] - self.peak_starts[i]) / self.freq
        return np.mean(t1s)
        
    def t2(self):
        t2s = np.zeros(len(self.s2))
        for i in self.s2:
            t2s[i] = (self.peak_stops[i] - self.peak_starts[i]) / self.freq
        return np.mean(t2s)
        
    def t12(self):
        s1_indexes = []
        for s1 in self.s1:
            if (s1 + 1) in self.s2:
                s1_indexes.append(s1)
        t12 = []
        for index in s1_indexes:
            t12_candidate = (self.peak_starts[index+1] - self.peak_stops[index]) * 1.0 / self.freq
            if t12_candidate < (60.0 / self.heart_rate):
                t12.append(t12_candidate)
        t12_mean = np.mean(t12)
        return t12_mean, t12_mean * 1.0 / ( 60.0 / self.heart_rate)
        
    def t21(self):
        s2_indexes = []
        for s2 in self.s2:
            if (s2 + 1) in self.s1:
                s2_indexes.append(s2)
        t21 = []
        for index in s2_indexes:
            t21_candidate = (self.peak_starts[index+1] - self.peak_stops[index]) * 1.0 / self.freq
            if t21_candidate < (60.0 / self.heart_rate):
                t21.append(t21_candidate)
        t21_mean = np.mean(t21)
        return t21_mean, t21_mean * 1.0 / ( 60.0 / self.heart_rate)
        
    def total_power_systole(self):
        s1_indexes = []
        for s1 in self.s1:
            if (s1 + 1) in self.s2:
                s1_indexes.append(s1)
        total_powers_systole = []
        for index in s1_indexes:
            if (self.peak_starts[index+1] - self.peak_stops[index]) < (60.0 / self.heart_rate):
                systole = self.signal[self.peak_stops[index] : self.peak_starts[index + 1]]
                total_power = 0
                for x in systole:
                    total_power = total_power + x**2
                    total_powers_systole.append(total_power)
        total_power_mean = np.mean(total_powers_systole)
        return total_power_mean
        