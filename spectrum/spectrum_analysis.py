import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored
from reader import reader


def spectrum_analysis(x, y, rank, tag):
    xf = np.fft.rfft(y) / x.shape[0]

    maxi = {}
    for i in range(xf.shape[0]):
        maxi[np.abs(xf[i])] = i
    maxi = [maxi[i] for i in sorted(maxi.keys())]

    print(colored("---------{}---------".format(tag), 'red'))
    waves = []
    for i in range(rank):
        n = xf[maxi[xf.shape[0] - 1 - i]]
        frequency = maxi[xf.shape[0] - 1 - i]
        print("{} * sin(2 * pi * {} * t)".format(np.abs(n), frequency))
        tmp = np.abs(n) * np.sin(2 * np.pi * frequency * x)
        waves.append(tmp)

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


def spectrum(files, config):
    for file_name in files:
        x, y = reader(file_name, config)
        x ,y = np.array(x) ,np.array(y)
        spectrum_analysis(x, y, config["show_spectrum"]["rank"], file_name)


'''
sample_rate = 100.0
t = np.arange(0, 1.0, 1.0 / sample_rate)
x = np.sin(2 * np.pi * 23 * t) + 2 * np.sin(2 * np.pi * 19 * t) - 3 * np.sin(2 * np.pi * 96 * t)
spectrum_analysis(t, x, 3, "test sample")
'''
