# -*- coding: utf-8 -*-
"""
Script for PCG signal parametrization.
Used parameters:
- FFT for S1 - only plots as far
- FFT for S2 - only plots as far
- FFT for other peaks detected - not yet
- spectral centroid of FFT
- Wigner distribution of tones - not yet, not sure
- STFT on whole signal - not yet
- total power during systole (between end of S1 and start of S2)
- Q-factor during systole - not yet
- t1 - S1 durarion
- t2 - S2 duration
- t12 - time between end of S1 and start of S2
- t21 - time between end of S2 and start of next S1
- mean12 - maximum of means in regions between S1 - S2 and S2 - S1

@author: Agnieszka Kaczmarczyk
"""

import numpy as np
import scipy
import matplotlib.pyplot as plt

class Parameters(object):
    def __init__(self, signal_PCG, freq, HR, S1, S2, S, peak_starts, peak_stops, signal_type):
        self.signal = signal_PCG
        self.freq = freq
        self.heart_rate = HR
        self.s1 = S1
        self.s2 = S2
        self.s_unknown = S
        self.peak_starts = peak_starts
        self.peak_stops = peak_stops
        self.signal_type = signal_type
            
    def s1_fft(self):
        SC = []
        
#        plt.figure()
        for i in self.s1:
            signal_s1 = self.signal[self.peak_starts[i] : self.peak_stops[i]]
            FFT = abs(scipy.fft(signal_s1))
            frequencies = scipy.fftpack.fftfreq(len(signal_s1), 1.0 / self.freq)
#            print self.spectral_centroid(FFT[0: len(FFT)/2], frequencies[0: len(FFT)/2])
            SC.append(self.spectral_centroid(FFT[0: len(FFT)/2], frequencies[0: len(FFT)/2]))

#            plt.plot(frequencies[0: len(FFT)/2], FFT[0: len(FFT)/2])
#            plt.title('S1')
#        plt.close()
        return np.mean(SC)
            
    def s2_fft(self):
        if self.signal_type == 1:
            SC = []
    
#            plt.figure()
            for i in self.s2:
                signal_s2 = self.signal[self.peak_starts[i] : self.peak_stops[i]]
                FFT = abs(scipy.fft(signal_s2))
                frequencies = scipy.fftpack.fftfreq(len(signal_s2), 1.0 / self.freq)
    #            print self.spectral_centroid(FFT[0: len(FFT)/2], frequencies[0: len(FFT)/2])
                SC.append(self.spectral_centroid(FFT[0: len(FFT)/2], frequencies[0: len(FFT)/2]))
                
#                plt.plot(frequencies[0: len(FFT)/2], FFT[0: len(FFT)/2])
#                plt.title('S2')
#            plt.close()
            return np.mean(SC)
        else:
            return -1
            
    def breaks_fft(self):
        if self.signal_type == 1:
            SC = []
            tones = self.s1 + self.s2 + self.s_unknown
            tones.sort()
    
            for i in tones[0 : len(tones) - 1]:
                signal_break = self.signal[self.peak_stops[i] : self.peak_starts[i + 1]]
                FFT = abs(scipy.fft(signal_break))
                frequencies = scipy.fftpack.fftfreq(len(signal_break), 1.0 / self.freq)
    #            print self.spectral_centroid(FFT[0: len(FFT)/2], frequencies[0: len(FFT)/2])
                SC.append(self.spectral_centroid(FFT[0: len(FFT)/2], frequencies[0: len(FFT)/2]))
                
#                plt.figure()
#                plt.plot(frequencies[0: len(FFT)/2], FFT[0: len(FFT)/2])
#                plt.title('break')
#            plt.close()
            print 'breaks fft: '
            print SC
            return np.mean(SC)
        else:
            return -1
                
            
    def spectral_centroid(self, FFT, frequencies):
        spectral_centroid_nominator = 0
        spectral_centroid_denominator = 0
        for index in range(0, len(FFT)):
            spectral_centroid_nominator = spectral_centroid_nominator + (frequencies[index] * FFT[index])
            spectral_centroid_denominator = spectral_centroid_denominator + FFT[index]
            
        return spectral_centroid_nominator / spectral_centroid_denominator
        
    def t1(self):
        t1s = []
        for i in self.s1:
            t1s.append((self.peak_stops[i] - self.peak_starts[i]) * 1.0 / self.freq)
        return np.mean(t1s)
        
    def t2(self):
        if self.signal_type == 1:
            t2s = []
            for i in self.s2:
                t2s.append((self.peak_stops[i] - self.peak_starts[i]) * 1.0 / self.freq)
            return np.mean(t2s)
        else:
            return -1
        
    def t12(self):
        if self.signal_type == 1:
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
        else:
            return -1
        
    def t21(self):
        if self.signal_type == 1:
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
        else:
            return -1
            
    def t_variance(self):
        tones = self.s1 + self.s2 + self.s_unknown
        tones_times = []
        for index in range(0, len(tones)):
            tones_times.append(self.peak_stops[index] - self.peak_starts[index])
        
        return np.std(tones_times)
        
    def tones_mean(self):
        tones = self.s1 + self.s2 + self.s_unknown
        tones_times = []
        for index in range(0, len(tones)):
            tones_times.append(self.peak_stops[index] - self.peak_starts[index])        
        tones_mean = np.mean(tones_times)
        tones_mean_percentage = tones_mean * 1.0 / (60.0 * self.freq/ self.heart_rate)
        
        return tones_mean, tones_mean_percentage
        
    def total_power_systole(self):
        if self.signal_type == 1:
            s1_indexes = []
            for s1 in self.s1:
                if (s1 + 1) in self.s2:
                    s1_indexes.append(s1)
            total_powers_systole = []
            for index in s1_indexes:
                if (self.peak_starts[index+1] - self.peak_stops[index]) * 1.0 / self.freq < (60.0 / self.heart_rate):      
                    systole = self.signal[self.peak_stops[index] : self.peak_starts[index + 1]]
                    total_power = 0
                    for x in systole:
                        total_power = total_power + x**2
                    half_cycle_frames = self.freq * (60.0 / self.heart_rate) / 2
                    half_cycle_frames_start = 0
                    if self.peak_stops[index] > half_cycle_frames:
                        half_cycle_frames_start = self.peak_stops[index] - half_cycle_frames
                    cycle = self.signal[half_cycle_frames_start : self.peak_stops[index] + half_cycle_frames]           
                    total_power_cycle = 0
                    for x in cycle:
                        total_power_cycle = total_power_cycle + x**2
                    # As percentage value of total power of the whole cycle
                    total_powers_systole.append(total_power / total_power_cycle)
            if not total_powers_systole:
                return 0
            else:
                total_power_mean = np.mean(total_powers_systole)
                return total_power_mean
        else:
            return -1   
        
    def energy(self, signal_in):
        return [x**2 for x in signal_in]        
        
    def breaks_power(self):
        tones_indexes = self.s1 + self.s2 + self.s_unknown
        tones_indexes.sort()
        breaks_powers = []
        breaks_powers_percentage = []
        cycle_length = int(60.0 * self.freq / self.heart_rate)
        
        for index in range(0, len(tones_indexes) - 1):
            if tones_indexes[index + 1] == tones_indexes[index] + 1:
                break_start = self.peak_stops[index]
                break_stop = self.peak_starts[index + 1]
                break_length = break_stop - break_start
                if break_length < cycle_length:
                    break_signal = self.signal[break_start : break_stop]
                    break_power = sum(self.energy(break_signal))
                    cycle = self.signal[break_start : break_start + cycle_length]
                    cycle_power = sum(self.energy(cycle))
                    breaks_powers.append(break_power)
                    breaks_powers_percentage.append(break_power * 1.0 / cycle_power)
        
        return np.mean(breaks_powers), np.mean(breaks_powers_percentage)
        
    def mean12(self):
        if self.signal_type == 1:
            systole_indexes = []
            for s1 in self.s1:
                if (s1 + 1) in self.s2:
                    systole_indexes.append(s1)
            systole_means = []
            for index in systole_indexes:
                if (self.peak_starts[index+1] - self.peak_stops[index]) * 1.0 / self.freq < (60.0 / self.heart_rate):
                    systole = self.signal[self.peak_stops[index] : self.peak_starts[index + 1]]
                    signal_mean = np.mean(systole)
                    systole_means.append(signal_mean)
            systole_mean = np.mean(systole_means)      
                    
            diastole_indexes = []
            for s2 in self.s2:
                if (s2 + 1) in self.s1:
                    diastole_indexes.append(s2)
            diastole_means = []
            for index in diastole_indexes:
                if (self.peak_starts[index+1] - self.peak_stops[index]) * 1.0 / self.freq < (60.0 / self.heart_rate):
                    diastole = self.signal[self.peak_stops[index] : self.peak_starts[index + 1]]
                    signal_mean = np.mean(diastole)
                    diastole_means.append(signal_mean)
            diastole_mean = np.mean(diastole_means)
            
            return max(systole_mean, diastole_mean)
        else:
            return -1