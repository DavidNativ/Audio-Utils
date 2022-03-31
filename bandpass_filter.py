from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
import scipy.signal as signal
import scipy.io.wavfile as wav

from find_n_harmonics import find_n_harmonics

def filter_n_harmonics(data, sr, harmo, Q=50):
    for f in harmo:
        # Sample rate and desired cutoff frequencies (in Hz).
        print(f"Filtering freq {round(f)}")

        #create the filter
        b_notch, a_notch = signal.iirnotch(f, Q, sr)
        data = signal.filtfilt(b_notch, a_notch, data)

        # #create the freq response for plotting
        # freq, h = signal.freqz(b_notch, a_notch, fs=2 * np.pi)
        # fig = plt.figure(figsize=(8, 6))
        #
        # # Plot magnitude response of the filter
        # plt.plot(freq * sr / (2 * np.pi), 20 * np.log10(abs(h)),
        #          'r', label='Bandpass filter', linewidth='2')
        #
        # plt.xlabel('Frequency [Hz]', fontsize=20)
        # plt.ylabel('Magnitude [dB]', fontsize=20)
        # plt.title('Notch Filter', fontsize=20)
        # plt.grid()
        # plt.show()
    return data


if __name__ == "__main__" :
    filename = './440.wav'
    #filename = './dog_bark.wav'

    ############# read_file
    print(f"Reading {filename}...")
    sr, data = wav.read(filename)

    ############ process stereo to mono (ToDO)
    try:
        channels = data.shape[1]
    except IndexError:
        channels = 1

    if channels > 1:
        print("WARNING Stereo File Detected.... we keep only one channel")
        data = data[:, 0]
    print(f"SR={sr} - Nb Channels={channels}")

    ########### filtering
    nb_harmo = 1
    main_harmo = find_n_harmonics(data, sr, nb_harmo, local_min_height=1, local_steps=1)
    res = filter_n_harmonics(data, sr, harmo=main_harmo)

    ######## write filtered signal
    wav.write('./res.wav', sr, res)


