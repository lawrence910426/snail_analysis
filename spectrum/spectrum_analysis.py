import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored


def spectrum_analysis(x, y, rank, tag):
    xf = np.fft.rfft(y) / x.shape[0]

    maxi = {}
    for i in range(xf.shape[0]):
        maxi[np.abs(xf[i])] = i
    maxi = [maxi[i] for i in sorted(maxi.keys())]

    if tag != "":
        print(colored("---------{}---------".format(tag), 'red'))
    waves, result = [], []
    for i in range(rank):
        n = xf[maxi[xf.shape[0] - 1 - i]]
        frequency = maxi[xf.shape[0] - 1 - i]
        tmp = np.abs(n) * np.sin(2 * np.pi * frequency * x)
        waves.append(tmp)
        result.append([np.abs(n), frequency])

        if tag != "":
            print("{} * sin(2 * pi * {} * t)".format(np.abs(n), frequency))

    if tag != "":
        plt.figure(figsize=(16, 16))
        plt.suptitle("Spectrum analysis of: " + tag, fontsize=20)
        plt.subplot(3, 1, 1)
        plt.plot(x, y, label="Original Data")
        plt.legend(loc='upper right')

        plt.subplot(3, 1, 2)
        plt.plot(range(xf.shape[0]), np.abs(xf), label="Spectrum Analysis")
        plt.legend(loc='upper right')

        plt.subplot(3, 1, 3)
        code = 1
        for wave in waves:
            plt.plot(x, wave, label="Ingredient {}".format(code))
            code += 1

        plt.legend(loc='upper right')
        plt.show()

    return result


def spectrum(file_name, x, y, config):
    return spectrum_analysis(x, y, config["show_spectrum"]["rank"],
                             file_name if config["show_spectrum"]["show"] else "")
'''
sample_rate = 1000.0
t = np.arange(0, 1.0, 1.0 / sample_rate)
x = np.sin(2 * np.pi * 18 * t)
spectrum_analysis(t, x, 2, "test sample")
'''