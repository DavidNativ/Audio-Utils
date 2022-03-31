import scipy.signal as signal
import scipy.io.wavfile as wav


### HELPER
def _find_n_local_harmonics(sig, freqs, n_max, local_steps, local_min_height):
    p = signal.find_peaks(x=sig, height=local_min_height)
    l = len(p[0])

    while l > n_max:
        local_min_height += local_steps
        p = signal.find_peaks(x=sig, height=local_min_height)
        l = len(p[0])
    #print(f"Found {l} harmonics with height={local_min_height}")
    return [(freqs[p[0]][i], p[1]['peak_heights'][i]) for i in range(l)]
###########

##############################################################################
# This function extracts the N main harmonics from a WAV file
# it proceeds by slicing the audio for short term freq domain conversion
#  extracts the local max and then proceed to the global max search
#
# Arguments:
# ----------
#       - filename
#       - n : number of harmonics to retrieve
#       - samples per slices : for computing FFT
#       - overlap : windowing
#       - n_local_max : number of harmonics to store for each slice
#       - local_steps & local_min_heights : parameters for finding peaks
################################################################################
def find_n_harmonics(data, sr, n, samples_per_slice=1024, overlap=100, n_local_max=5, local_steps=1, local_min_height=1):

    ########### compute the spectrograms for each slice of M values
    freqs, times, Sx = signal.spectrogram(data, fs=sr, window='hanning',
                                          nperseg=samples_per_slice, noverlap=samples_per_slice - overlap,
                                          detrend=False, scaling='spectrum',
                                          mode='magnitude')
    Sx = Sx.T
    # print(f'freqs:{freqs.shape}  - times:{times.shape}  - Sx: {Sx.shape}')

    #finds all the harmonics
    # iterate on all the samples and create a list of all the (freq, amp)
    res = []
    for sl in range(len(Sx)):
        local_max = _find_n_local_harmonics(Sx[sl], freqs, n_local_max, local_steps=local_steps, local_min_height=local_min_height)
        for lm in local_max:
            res.append(lm)

    # sort according to the amplitude
    res.sort(key=lambda x: x[1])

    # invert sort order for descending
    max = res[::-1]
    # extract only freq
    max = [e[0] for e in max]
    # remove duplicates
    max = list(dict.fromkeys(max))
    return max[:n]
#####################################################################################


"""
if __name__ == "__main__" :
    filename = './dog_bark.wav'
    nb_harmo = 5
    print(find_n_harmonics(filename, nb_harmo))
"""