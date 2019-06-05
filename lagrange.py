import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

x = []
y1, y2 = [], []

with open('1.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    counter = 0
    for row in rows:
        if not (counter == 0 or counter == 1):
            x.append(float(row[0]))
            y1.append(float(row[3]))
            y2.append(float(row[4]))
        counter += 1

f2 = lagrange(x, y2)
graph2 = [f2(i) for i in range(100)]
plt.plot([i for i in range(100)], graph2)
plt.show()
