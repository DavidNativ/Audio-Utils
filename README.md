# Audio Utils : a Python library for classic audio utils


### find_n_harmonics(data, sr, n, samples_per_slice=1024, overlap=100, n_local_max=5, local_steps=1, local_min_height=1):
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

             - local_steps, local_min_height : parameters for the find_peak function. If no harmonic is found, tweak those param
       
### filter_n_harmonics(data, sr, harmo, Q=50):
Function that writes a wav file containing the audio data filtered by bandstop filters centered on the freq stored in harmo

       Arguments:
       ----------
              - data: a numpy array that contains the audio data (MONO)
              - sr : sample rate
              - harmo : an array containing the center frequencies of the filters
              - Q: quality factor of the filters
       
       
