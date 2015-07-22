# -*- coding: utf-8 -*-
"""
Main.

@author: Agnieszka Kaczmarczyk
"""

import wave_operations as wo
import preprocessing as pr
import segmentation as segm


filepath = "103_1305031931979_D2.wav"
signal_PCG, params = wo.read_wavefile(filepath)
freq = 4000

# Preprocessing of the signal: decimation.
signal_PCG = pr.decimate(signal_PCG, params, freq)

# Preprocessing of the signal: normalization.
signal_PCG = pr.normalize(signal_PCG)

# Preprocessing of the signal: filtering.
cutoff = 80
signal_PCG = pr.butter_lowpass_filter(signal_PCG, cutoff, freq, 1)

# Shannon energy envelope
shannon_envelope = segm.shannon_energy_envelope(signal_PCG, freq)
wo.plot_wave_signal(shannon_envelope, freq)
