import scipy.fft
import numpy as np
import matplotlib.pyplot as plt

class WavTable:
    def __init__(self, nb_of_samples=64, function=np.sin):
        # nb of samples in a WT scheme
        self._nb_of_samples = nb_of_samples
        # WT scheme
        self._function = function
        # WT
        self._wavtable = np.zeros((self.nb_of_samples, ))
        self._build_wavtable()

    def __str__(self):
        return f"WavTable \nNumber of samples: {self._nb_of_samples} - function: {self._function}"

    @property
    def function(self):
        print(f"{self._function}")

    @function.setter
    def function(self, fun):
        self._function = fun
        self._build_wavtable()

    @property
    def wavtable(self):
        return self._wavtable

    @property
    def nb_of_samples(self):
        return self._nb_of_samples

    @nb_of_samples.setter
    def nb_of_samples(self, val):
        self._nb_of_samples = val
        self._build_wavtable()


    def _build_wavtable(self):
        self._wavtable = np.zeros((self._nb_of_samples, ))
        # fill it
        print(self._function)
        for sample in range(self._nb_of_samples):
            self.wavtable[sample] = self._function(2 * np.pi * sample / self._nb_of_samples)



    def plot(self, buffer):
        spec = scipy.fft.fft(buffer)
        print(spec.shape)


        x = (np.linspace(20, 512, num=1024))  # np.log
        fig, ax = plt.subplots(3)
        ax[0].plot(x, np.log10(np.abs(spec[:len(x)])))


        ax[1].plot(buffer[512:812])
        X = np.linspace(0, self._nb_of_samples, num=self._nb_of_samples, endpoint=False)
        ax[2].plot(X, self._wavtable)

        plt.show()



    def linear_extrapolation(self, index):
        trunc = np.floor(index)
        index_inf = trunc
        index_sup = (trunc + 1) % self._nb_of_samples

        slope = self._function(index_sup) - self._function(index_inf)  # / (index_sup - index_inf)
        offset = self._function(index_inf) - slope * index_inf

        return slope * index + offset

