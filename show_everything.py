import matplotlib.pyplot as plt
import math
from scipy import stats
from termcolor import colored
import numpy as np


def show_everything(x, y, env, spec ,tag):
    env[0], env[1] = (env[0][0] + env[1][0]) / 2, (env[0][1] + env[1][1]) / 2
    spec_len = len(spec)
    freq = sum([spec[i][0] * spec[i][1] for i in range(spec_len)]) / sum([spec[i][0] for i in range(spec_len)])
    exec = lambda t, freq_t: env[0] * np.exp(env[1] * t) * np.sin(2 * np.pi * freq * freq_t)

    virtual = []
    for i in range(x.shape[0]):
        virtual.append(exec(x[i], i / x.shape[0]))

    print(colored("---------{}---------".format(tag), 'red'))
    print("Trajectory: {} * e^({} * t) * sin(2 * pi * t * {})".format(env[0], env[1], freq))
    plt.plot(x, y)
    plt.plot(x, virtual)
    plt.show()
