import scipy.io.wavfile as wav

from wavtable import *
from fftPlot import *

import argparse
import sounddevice as sd



def generate_buffer(length, freq, amplitude, wt, sr=44100, linex=True):
    buffer = np.zeros((sr * length, ))
    # apply condition once for avoiding bool eval at each step
    if not linex:
        k = 0
        for i in range(len(buffer)):
            k_inc = wt.nb_of_samples * freq / sr
            k += k_inc
            k %= wt.nb_of_samples
            buffer[i] = amplitude * wt.wavtable[int(np.floor(k))]
            #buffer[i][1] = buffer[i][0]
        return buffer
    else:
        k = 0
        for i in range(len(buffer)):
            k_inc = wt.nb_of_samples * freq / sr
            k += k_inc
            k %= wt.nb_of_samples
            buffer[i] = amplitude * wt.linear_extrapolation(k)
            #buffer[i][1] = buffer[i][0]
        return buffer


def apply_fade_in_out(length_fade_in, length_fade_out, buffer, sr=44100):
    #applying windowing
    length_fade_in = 0.5 #sec
    win_fade_in = np.zeros((int(np.ceil(length_fade_in * sr)), 1))


    x = np.linspace(0, np.pi/2, num=int(np.ceil(length_fade_in*sr)))
    win_fade_in = np.sin(x)
    win_fade_out = win_fade_in[::-1]

    buffer[:len(win_fade_in)]   *= win_fade_in
    buffer[-len(win_fade_out):] *= win_fade_out

    return buffer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, required=False, help='Output file')
    parser.add_argument('--resolution', type=int, required=False, help='Wav Table number of samples', default=64)
    parser.add_argument('--sr',         type=int, required=False, help='Generated wav Sample Rate', default=44100)
    parser.add_argument('--freq',       type=int, required=False, help='Frequency of the generated wav', default=440)
    parser.add_argument('--amplitude',  type=float, required=False, help='Amplitude of the generated wav', default=0.2)
    parser.add_argument('--length',     type=float, required=False, help='Length of the generated wav', default=3)
    parser.add_argument('--fade_length',type=float, required=False, help='Fades in/out length (default: 0.5s)', default=0.5)
    parser.add_argument('--plot',  required=False, help='Plot the wave table',           action='store_true')
    parser.add_argument('--fade',  required=False, help='Apply fade in and fade out' ,   action='store_true')
    parser.add_argument('--linex', required=False, help='Apply linear extrapolation' ,   action='store_true')
    parser.add_argument('--function', choices=['sin', 'saw', 'square'], required=False, help='Type of function (sin, square, saw', default='sin')
    args = parser.parse_args()

    ## audio file params
    length = args.length
    sr = args.sr
    freq = args.freq
    amplitude = args.amplitude
    resolution = args.resolution
    length_fade = args.fade_length



    #wt = WavTable(function=signal.square)
    #wt = WavTable(function=signal.sawtooth, nb_of_samples=1024)
    wt = WavTable(function=np.sin, nb_of_samples=resolution)
    print(wt)

    #filling the audio buffer
    buffer = generate_buffer(length, freq, amplitude, wt, sr, args.linex)

    if args.fade:
        apply_fade_in_out(length_fade_in=length_fade, length_fade_out=length_fade, buffer=buffer, sr=sr)


    if args.plot:
        wt.plot(buffer)
        fftPlot(buffer)


    sd.play(buffer, samplerate=sr)
    import time
    time.sleep(length)
    sd.stop(ignore_errors=True)

    if args.output:
        wav.write(args.output, args.sr, buffer)

