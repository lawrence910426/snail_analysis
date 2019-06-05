import numpy as np
import csv
import matplotlib.pyplot as plt
import math
from scipy import stats
import sys


def show_curve(x, y, mini_diff=5, mini_len=3):
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
                        upper_v.append(np.log(y[i - 1]))
                    else:
                        lower_i.append(x[i - 1])
                        lower_v.append(np.log(-y[i - 1]))
                monotone_q = [monotone_q[len(monotone_q) - 1], y[i]]
        else:
            if monotone_q[len(monotone_q) - 1] > y[i]:
                monotone_q.append(y[i])
            else:
                if np.abs(monotone_q[len(monotone_q) - 1] - monotone_q[0]) > mini_diff and len(monotone_q) > mini_len:
                    if y[i] > 0:
                        upper_i.append(x[i - 1])
                        upper_v.append(np.log(y[i - 1]))
                    else:
                        lower_i.append(x[i - 1])
                        lower_v.append(np.log(-y[i - 1]))
                monotone_q = [monotone_q[len(monotone_q) - 1], y[i]]

    alpha_up, beta_up, _, _, _ = stats.linregress(upper_i, upper_v)
    alpha_low, beta_low, _, _, _ = stats.linregress(lower_i, lower_v)

    print("Envelope(up): e^({} * x + {})".format(alpha_up, beta_up))
    print("Envelope(down): -e^({} * x + {})".format(alpha_low, beta_low))

    plt.plot(x, y)
    plt.plot(upper_i, [math.exp(alpha_up * item + beta_up) for item in upper_i], label="Envelope(up)")
    plt.plot(lower_i, [-math.exp(alpha_low * item + beta_low) for item in lower_i], label="Envelope(down)")
    plt.scatter(upper_i, np.exp(upper_v), label="Values found(up)")
    plt.scatter(lower_i, -np.exp(lower_v), label="Values found(down)")
    plt.legend()
    plt.show()


file_name = input(u"輸入被分析的檔案\n")
leng = int(input(u"輸入分析列數\n"))

x = []
y1, y2 = [], []

with open(file_name, newline='') as csvfile:
    rows = csv.reader(csvfile)
    counter = 0
    for row in rows:
        if not (counter == 0 or counter == 1):
            x.append(float(row[0]))
            y1.append(float(row[3]))
            y2.append(float(row[4]))
        if counter >= leng:
            break
        counter += 1
x = np.array(x)
y1, y2 = np.array(y1), np.array(y2)
show_curve(x, y2, )
