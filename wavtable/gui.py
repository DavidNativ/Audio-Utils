import numpy as np
import streamlit as st
from wavtable import *
from main import *
import scipy.signal as signal


def generate(fun, length, sr, freq, amplitude, resolution, linex, fade):
    ## audio file params
    length_fade = 3

    # wt = WavTable(function=signal.square)
    # wt = WavTable(function=signal.sawtooth, nb_of_samples=1024)
    if fun == 'sin':
        function = np.sin
    elif fun == 'square':
        function = signal.square
    elif fun == 'saw':
        function = signal.sawtooth


    wt = WavTable(function=function, nb_of_samples=resolution)

    # filling the audio buffer
    buffer = generate_buffer(length=length, freq=freq, amplitude=amplitude, wt=wt, sr=sr, linex=linex)

    if fade:
        apply_fade_in_out(length_fade_in=length_fade, length_fade_out=length_fade, buffer=buffer, sr=sr)

    # if args.plot:
    #     wt.plot(buffer)
    #     fftPlot(buffer)

    sd.play(buffer, samplerate=sr)
    import time
    time.sleep(length)
    sd.stop(ignore_errors=True)

    # if args.output:
    #     wav.write(args.output, args.sr, buffer)


st.title("WAVE Table: Signal Generator")
st.markdown("##Salut les **enfants**")


freq = st.slider("Frequency", 20, 8000, 440)
amplitude = st.slider("amplitude", 0., 0.8, 0.125)
resolution = st.slider("resolution", 4, 1025, 16)
length = int(np.ceil(st.slider("Length", 0.5, 5., 3.)))
sr = int(st.selectbox("SampleRate", ["22050", "11025", "44100"]))
fun = st.radio("Function", ['sin', 'square', 'saw'])
linex = st.checkbox("Linear Extrapolation", True)
fade = st.checkbox("FadeIN & FadeOUT", True)

if st.button("Generate !"):
    st.subheader("Features")
    st.write(f'freq {freq}Hz - length {length}s - sr {sr} - fade {fade} - linex {linex}')
    generate(length=length, sr=sr, freq=freq, amplitude=amplitude, resolution=resolution, linex=linex, fade=fade, fun=fun)


