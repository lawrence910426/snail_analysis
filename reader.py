import csv

def reader(file_name, config):
    x, y = [], []
    with open(file_name, newline='') as csvfile:
        leng = config["global"]["rows"]["value"]
        rows = csv.reader(csvfile)
        rows = [[i for i in row] for row in rows]
        for i in range(config["global"]["x"]["row"], config["global"]["x"]["row"] + leng):
            x.append(float(rows[i][config["global"]["x"]["column"]]))
        for i in range(config["global"]["y"]["row"], config["global"]["y"]["row"] + leng):
            y.append(float(rows[i][config["global"]["y"]["column"]]))
    return x, y
