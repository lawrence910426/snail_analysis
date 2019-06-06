import re
import bisect
from termcolor import colored
import numpy as np
from envelope.segment_tree import *
import pandas as pd


def monotone(x, y, mini_diff, mini_len):
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


def manual(x, y):
    upper_i, upper_v, lower_i, lower_v = [], [], [], []
    while True:
        tick = input("Input the peak time tick (Input nothing if you want to stop):")
        if tick == "" or re.match("^[0-9]+?.[0-9]+?$", tick) is None:
            print(colored("Terminated ,input was done.", 'red'))
            break
        tick = float(tick)
        l = bisect.bisect_left(x, tick)
        if x[l] == tick:
            if y[l] > 0:
                upper_i.append(x[l])
                upper_v.append(y[l])
                print("Found a upper peak ({} ,{})".format(x[l], y[l]))
            else:
                lower_i.append(x[l])
                lower_v.append(-y[l])
                print("Found a lower peak ({} ,{})".format(x[l], y[l]))
        else:
            text = "Unable to find the tick ,the latest is {}".format(x[l])
            print(colored(text, 'red'))
    return upper_i, upper_v, lower_i, lower_v


def from_file(x, y, fname):
    upper_i, upper_v, lower_i, lower_v = [], [], [], []
    with open(fname, "r") as f:
        while f.readable():
            line = f.readline()
            try:
                line = float(line)
            except:  # Yeah fuck you i am gonna use bare except
                break
            ptr = bisect.bisect_left(x, line)
            if y[ptr] > 0:
                upper_i.append(x[ptr])
                upper_v.append(y[ptr])
            else:
                lower_i.append(x[ptr])
                lower_v.append(-y[ptr])
    return upper_i, upper_v, lower_i, lower_v


def range_query(x, y, window, rank):
    up_st = segment_tree(y, 0, len(y), lambda a, b, xx: a if xx[a] > xx[b] else b)
    low_st = segment_tree(y, 0, len(y), lambda a, b, xx: a if xx[a] < xx[b] else b)
    up_rank, low_rank = [[0, i] for i in range(len(y))], [[0, i] for i in range(len(y))]
    for i in range(len(y)):
        for j in range(window):
            lbound, ubound = i - j if i - j > 0 else 0, i + j if i + j < len(y) - 1 else len(y) - 1
            up_rank[up_st.query(lbound, ubound + 1)][0] -= 1
            low_rank[low_st.query(lbound, ubound + 1)][0] -= 1

    up_rank = sorted(up_rank, key=lambda x: x[0])
    low_rank = sorted(low_rank, key=lambda x: x[0])

    upper_i, upper_v = [x[up_rank[i][1]] for i in range(rank)], [y[up_rank[i][1]] for i in range(rank)]
    lower_i, lower_v = [x[low_rank[i][1]] for i in range(rank)], [-y[low_rank[i][1]] for i in range(rank)]
    return upper_i, upper_v, lower_i, lower_v
