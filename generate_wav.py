import scipy.signal as signal
import scipy.io.wavfile as wav
import numpy as np

#### WARNING !!!
# this is a deprecated way of creating a sine wav
# it is using a lot of memory
# WAVTABLE would be better




################################
# This function generates a wav file of sample rate sr. It is composed of addition of the freq present
# in the list of tuples freqs, each tuple being a couple (Amplitude, Frequency) [amp in [0,1] - freq in Hz]
#
# Arg :
#   - filename : path and file name to write the resulting wav
#   - length : length in seconds
#   - sr : sample rate (default 44.1 kHz)
#   - freqs : a list of couple (Amplitude, Frequency) w/ amp in [0,1]
################################

def generate_sine_waves(filename, length, sr=44100, freqs=[(0.2, 440)]):
    #initialize the data
    data = np.zeros((length * sr,) )

    #filling
    for (A,f) in freqs:
        for s in range(length * sr):
            data[s] += A * np.sin(2 * np.pi * f * s / sr)

    #writing the audio file
    wav.write(filename, sr, data)
    print("Wav file successfully written")
