# Audio Utils : a Python library for classic audio utils

##### generate_sine_waves(filename, length, sr=44100, freqs=[(0.2, 440)])
This function generates a wav file of sample rate sr. It is composed of addition of the freq present
in the list of tuples freqs, each tuple being a couple (Amplitude, Frequency) [amp in [0,1] - freq in Hz]

	Arguments :
	----------
		  - filename : path and file name to write the resulting wav
		  - length : length in seconds
		  - sr : sample rate (default 44.1 kHz)
		  - freqs : a list of couple (Amplitude, Frequency) w/ amp in [0,1]
#### WARNING !!!
this is a deprecated way of creating a sine wav
it is using a lot of memory
WAVTABLE would be better



##### find_n_harmonics(data, sr, n, samples_per_slice=1024, overlap=100, n_local_max=5, local_steps=1, local_min_height=1):
Function that extracts the n main frequencies of a wav file

This function extracts the N main harmonics from a WAV file
it proceeds by slicing the audio for short term freq domain conversion
 extracts the local max and then proceed to the global max search

      Arguments:
      ----------
             - data: a numpy array that contains the audio data (MONO)
             - sr : sample rate
             - n : number of harmonics to retrieve

             - samples per slices : for computing FFT (default=1024)
             - overlap : windowing (default=100)
             - n_local_max : number of harmonics to store for each slice (default=5)

             - local_steps, local_min_height : parameters for the find_peak function. 
               If no harmonic is found, tweak those param
       
##### filter_n_harmonics(data, sr, harmo, Q=50):
Function that writes a wav file containing the audio data filtered by bandstop filters centered on the freq stored in harmo

       Arguments:
       ----------
              - data: a numpy array that contains the audio data (MONO)
              - sr : sample rate
              - harmo : an array containing the center frequencies of the filters
              - Q: quality factor of the filters
       
       
## Examples
filename = './440.wav'  
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

########### finding the n main frequencies
nb_harmo = 2
main_harmo = find_n_harmonics(data, sr, nb_harmo, local_min_height=1, local_steps=1)

########### filtering
res = filter_n_harmonics(data, sr, harmo=main_harmo)

######## writing filtered signal
wav.write('./res.wav', sr, res)



