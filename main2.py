# -*- coding: utf-8 -*-
"""
Image processing try.

@author: Agnieszka Kaczmarczyk
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy
import cv2
from scipy import ndimage
import wave_operations as wo
import preprocessing as pr
import segmentation as segm
import stft_module as stft
import os
from os import listdir
from os.path import isfile, join

plt.close('all')
freq = 4000

my_path = os.getcwd() + '\\image'
wave_files = [ f for f in listdir(my_path) if isfile(join(my_path,f)) ]

for wave_file in wave_files[0:50]:
    wave_file_path = my_path + '\\' + wave_file
    print wave_file_path
    signal_PCG, params = wo.read_wavefile(wave_file_path)
    signal_PCG[0 : int(params[2] * 0.3)] = 0
    signal_PCG[len(signal_PCG) - int(params[2] * 0.3) : ] = 0
    
    # Preprocessing of the signal: filtering.
    cutoff = 195
    signal_PCG = pr.butter_lowpass_filter(signal_PCG, cutoff, freq, 2)
    # Preprocessing of the signal: decimation.
    signal_PCG = pr.decimate(signal_PCG, params, freq)
				
    X = stft.stft2(signal_PCG, freq, 0.06, 0.02)
    # Create matrix A as absolute normalized X.
    A = X[:][:]
    
    v = len(A[0])
    for i in range(0, int(v * 5.0 / 6)):
        A = scipy.delete(A, int(v * 1.0 / 6), 1)  
        
    A = A.T
    A = scipy.absolute(A)
    
    maximum = A.max()
    A = A * (1.0 / maximum) 
    print np.mean(A)
    
    plt.figure()
    plt.imshow(A, origin='lower', aspect='auto',
                 interpolation='nearest')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()    
    
    thresh = cv2.threshold(A.astype('float32'), 22 * np.mean(A), 1,cv2.THRESH_BINARY) 
    
    plt.figure()
    plt.imshow(thresh[1], origin='lower', aspect='auto',
                 interpolation='nearest')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()    

    # Create matrix B as peaks determinator.
    B = np.copy(thresh[1])
    
    # Create matrix D as dilated matrix B.    
    D = ndimage.binary_dilation(B).astype(B.dtype)   
    D = ndimage.binary_dilation(D).astype(B.dtype)  
    D = ndimage.binary_dilation(D).astype(B.dtype) 
    D = ndimage.binary_dilation(D).astype(B.dtype) 
    D = ndimage.binary_dilation(D).astype(B.dtype) 
    D = ndimage.binary_dilation(D).astype(B.dtype)
    D = ndimage.binary_dilation(D).astype(B.dtype)
    D = ndimage.binary_dilation(D).astype(B.dtype)
    
    plt.figure()
    plt.imshow(D, origin='lower', aspect='auto',
                 interpolation='nearest')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()
    
    cols = len(B[0])
    rows = len(B)
    sums = np.zeros(cols)
    for row in range(0, rows):
        for col in range(0, cols):
            if B[row][col] == 1:
                B[:,col] = 1
    
    # Create matrix C as peaks lines centers.
    C = ndimage.binary_dilation(B).astype(B.dtype)   
    C = ndimage.binary_dilation(C).astype(B.dtype)  
    C = ndimage.binary_dilation(C).astype(B.dtype) 
    
    plt.figure()
    plt.imshow(C, origin='lower', aspect='auto',
                 interpolation='nearest')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()   
    
    thresh2 = cv2.threshold(A.astype('float32'), 2 * np.mean(A), 20 * np.mean(A),cv2.THRESH_BINARY) 
    
    # Create matrix E as high frequencies between peaks.
    E = thresh2[1] - C - D
    E[0:3, :] = 0
    cols = len(E[0])
    rows = len(E)
    for row in range(0, rows):
        for col in range(0, cols):
            if E[row][col] < 0:
                E[row][col] = 0
    
    plt.figure()
    plt.imshow(E, origin='lower', aspect='auto',
                 interpolation='nearest')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()     
    
    continue    
    
    A = ndimage.binary_dilation(A).astype(A.dtype)
    
    plt.figure()
    plt.imshow(A, origin='lower', aspect='auto',
                 interpolation='nearest')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()    
    
    # Preprocessing of the signal: normalization.
    signal_PCG = pr.normalize(signal_PCG)
    
    signal_PCG_original = np.copy(signal_PCG)
    
    # Denoising histogram using histogram method.
    signal_PCG = segm.histogram_denoising(signal_PCG)
    
    # Determine heart rate.
    heart_rate = segm.heart_rate(signal_PCG, freq) 