import csv
import matplotlib.pyplot as plt
import math
from scipy import stats
from envelope.envelope_import import *


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


def rmq():
    return [0], [0], [0], [0]


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
        if config["show_envelope"]["mono_q"]["activate"]:
            mq_attr = config["show_envelope"]["mono_q"]
            a, b, c, d = monotone(x, y, mq_attr["mini_diff"], mq_attr["mini_len"])
        elif config["show_envelope"]["rmq"]["activate"]:
            rmq_attr = config["show_envelope"]["rmq"]
            a, b, c, d = range_query(x, y, rmq_attr["window"], rmq_attr["rank"])
        elif config["show_envelope"]["manual"]["activate"]:
            a, b, c, d = manual(x, y)
        elif config["show_envelope"]["file"]["activate"]:
            a, b, c, d = from_file(x, y, config["show_envelope"]["file"]["location"])
        up_tmp, low_tmp = {a[i]: b[i] for i in range(len(a))}, {c[i]: d[i] for i in range(len(c))}
        a, c = sorted(up_tmp.keys()), sorted(low_tmp.keys())
        b, d = [up_tmp[k] for k in a], [low_tmp[k] for k in c]
        show_curve(a, b, c, d, x, y)