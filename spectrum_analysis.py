import numpy as np
import csv
import matplotlib.pyplot as plt


def show_fft(x, y, gets):
    sample_rate = x[x.shape[0] - 1] / (x[1] - x[0])
    xf = np.fft.rfft(y) / x.shape[0]

    maxi = {}
    for i in range(xf.shape[0]):
        maxi[np.abs(xf[i])] = i
    maxi = [maxi[i] for i in sorted(maxi.keys())]

    waves = []
    for i in range(gets):
        n = xf[maxi[xf.shape[0] - 1 - i]]
        frequency = maxi[xf.shape[0] - 1 - i]
        print("{} * sin(2 * pi * {} * t)".format(np.abs(n), frequency))
        tmp = np.abs(n) * np.sin(2 * np.pi * frequency * x)
        waves.append(tmp)

    plt.subplot(3, 1, 1)
    plt.plot(x, y, label="Original Data")
    plt.legend(loc='upper right')

    plt.subplot(3, 1, 2)
    plt.plot(range(xf.shape[0]), np.abs(xf), label="Spectrum Analysis")
    plt.legend(loc='upper right')

    plt.subplot(3, 1, 3)
    for wave in waves:
        plt.plot(x, wave, label="Ingredient of original data")
    plt.legend(loc='upper right')

    plt.show()


file_name = input(u"請輸入要分析的檔案名稱\n")
rank = int(input(u"輸出前幾高的波\n"))
leng = int(input(u"取值幾列\n"))

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
show_fft(x, y2, rank)

'''
sample_rate = 100.0
t = np.arange(0, 1.0, 1.0 / sample_rate)
x = np.sin(2 * np.pi * 23 * t) + 2 * np.sin(2 * np.pi * 19 * t)# - 3 * np.sin(2 * np.pi * 96 * t)
show_fft(t, x)
'''
