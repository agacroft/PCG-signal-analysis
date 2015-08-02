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
import stft_module as stft

plt.close('all')
freq = 4000

def murmurs(signal_PCG, freq, starts, stops, s1, s2, s, heart_rate):
				
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
    
    plt.figure()
    plt.imshow(A, origin='lower', aspect='auto',
                 interpolation='nearest')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()    
    
    thresh = cv2.threshold(A.astype('float32'), 18 * np.mean(A), 1,cv2.THRESH_BINARY) 
    
#    plt.figure()
#    plt.imshow(thresh[1], origin='lower', aspect='auto',
#                 interpolation='nearest')
#    plt.xlabel('Time')
#    plt.ylabel('Frequency')
#    plt.show()    

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
    
#    plt.figure()
#    plt.imshow(D, origin='lower', aspect='auto',
#                 interpolation='nearest')
#    plt.xlabel('Time')
#    plt.ylabel('Frequency')
#    plt.show()
    
    cols = len(B[0])
    rows = len(B)
    for row in range(0, rows):
        for col in range(0, cols):
            if B[row][col] == 1:
                B[:,col] = 1
    
    # Create matrix C as peaks lines centers.
    C = ndimage.binary_dilation(B).astype(B.dtype)   
    C = ndimage.binary_dilation(C).astype(B.dtype)  
    C = ndimage.binary_dilation(C).astype(B.dtype) 
    
#    plt.figure()
#    plt.imshow(C, origin='lower', aspect='auto',
#                 interpolation='nearest')
#    plt.xlabel('Time')
#    plt.ylabel('Frequency')
#    plt.show()   
    
    thresh2 = cv2.threshold(A.astype('float32'), 2 * np.mean(A), 18 * np.mean(A),cv2.THRESH_BINARY) 
    
    # Create matrix E as high frequencies between peaks.
    E = thresh2[1] - C - D
    E[0:6, :] = 0
    cols = len(E[0])
    rows = len(E)
    for row in range(0, rows):
        for col in range(0, cols):
            if E[row][col] < 0:
                E[row][col] = 0

    E = ndimage.binary_dilation(E).astype(E.dtype)
    E = ndimage.binary_closing(E).astype(E.dtype)

    E2, contours, hierarchy = cv2.findContours(E.astype(np.uint8),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(E2, contours, -1, (0,255,0), 3)    
    
    cx = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5.0:
            M = cv2.moments(cnt)
            cx.append(int(M['m10']/M['m00']))
        
    tx = []
    for index in range(0, len(cx)):
        tx.append(cx[index] * 0.02 + 0.03)
    
    plt.figure()
    plt.imshow(E, origin='lower', aspect='auto',
                 interpolation='nearest')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()     
    
    murmur_candidates_t = np.copy(tx)
    murmur_candidates_t.sort()
    tones_t = calculate_tone_times(starts, stops, s1, s2, s)
    
    print 'tones times:'
    print ["%0.2f" % i for i in tones_t]
    print 'murmur candidates times:'
    print ["%0.2f" % i for i in murmur_candidates_t]    
    
    murmur_candidates_t = remove_peaks_from_candidates(tones_t, murmur_candidates_t)
    print 'murmur candidates times:'
    print ["%0.2f" % i for i in murmur_candidates_t]  
    
    return tx
    
    
def calculate_tone_times(starts, stops, s1, s2, s):
    tones = s1 + s2 + s
    tones.sort()
    tones_t = []
    for tone in tones:
        tones_t.append((starts[tone] + (stops[tone] - starts[tone])/2) * 1.0 / freq)
        
    return tones_t
    
def remove_peaks_from_candidates(tones_t, candidates_t):
    murmurs_t = []
    for t in candidates_t:
        is_peak = False
        for peak_t in tones_t:
            if abs(peak_t - t) < 0.05:
                is_peak = True
        if is_peak == False:
            murmurs_t.append(t)
            
    return murmurs_t