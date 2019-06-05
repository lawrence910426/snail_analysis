import numpy as np
import csv
import matplotlib.pyplot as plt
import math
from scipy import stats
import sys


def monotone(x, y, mini_diff=5, mini_len=3):
    upper_i, upper_v, lower_i, lower_v = [], [], [], []
    monotone_q = [y[0], y[1]]

    for i in range(2, len(y)):
        if monotone_q[0] < monotone_q[1]:
            if monotone_q[len(monotone_q) - 1] < y[i]:
                monotone_q.append(y[i])
            else:
                if np.abs(monotone_q[len(monotone_q) - 1] - monotone_q[0]) > mini_diff and len(monotone_q) > mini_len:
                    if y[i] > 0:
                        upper_i.append(x[i - 1])
                        upper_v.append(y[i - 1])
                    else:
                        lower_i.append(x[i - 1])
                        lower_v.append(-y[i - 1])
                monotone_q = [monotone_q[len(monotone_q) - 1], y[i]]
        else:
            if monotone_q[len(monotone_q) - 1] > y[i]:
                monotone_q.append(y[i])
            else:
                if np.abs(monotone_q[len(monotone_q) - 1] - monotone_q[0]) > mini_diff and len(monotone_q) > mini_len:
                    if y[i] > 0:
                        upper_i.append(x[i - 1])
                        upper_v.append(y[i - 1])
                    else:
                        lower_i.append(x[i - 1])
                        lower_v.append(-y[i - 1])
                monotone_q = [monotone_q[len(monotone_q) - 1], y[i]]
    return upper_i, upper_v, lower_i, lower_v


def show_curve(upper_i, upper_v, lower_i, lower_v, rawx, rawy):
    alpha_up, beta_up, _, _, _ = stats.linregress(upper_i, np.log(upper_v))
    alpha_low, beta_low, _, _, _ = stats.linregress(lower_i, np.log(lower_v))

    print("Envelope(up): e^({} * x + {})".format(alpha_up, beta_up))
    print("Envelope(down): -e^({} * x + {})".format(alpha_low, beta_low))

    plt.plot(rawx, rawy)
    plt.plot(upper_i, [math.exp(alpha_up * item + beta_up) for item in upper_i], label="Envelope(up)")
    plt.plot(lower_i, [-math.exp(alpha_low * item + beta_low) for item in lower_i], label="Envelope(down)")
    plt.scatter(upper_i, upper_v, label="Values found(up)")
    plt.scatter(lower_i, np.negative(lower_v), label="Values found(down)")
    plt.legend()
    plt.show()


def show_envelope(files, config):
    x, y = [], []
    for file_name in files:
        with open(file_name, newline='') as csvfile:
            leng = config["global"]["rows"]["value"]
            rows = csv.reader(csvfile)
            rows = [[i for i in row] for row in rows]
            for i in range(config["global"]["x"]["row"], config["global"]["x"]["row"] + leng):
                x.append(float(rows[i][config["global"]["x"]["column"]]))
            for i in range(config["global"]["y"]["row"], config["global"]["y"]["row"] + leng):
                y.append(float(rows[i][config["global"]["y"]["column"]]))
        x, y = np.array(x), np.array(y)
        a, b, c, d = monotone(x, y)
        show_curve(a, b, c, d, x, y)
