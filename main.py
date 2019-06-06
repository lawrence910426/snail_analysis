import os
import json
import glob
from envelope.show_envelope import show_envelope
from spectrum.spectrum_analysis import spectrum

config = {
    "show_envelope": {
        "execute": True,
        "mono_q": {
            "activate": False,
            "mini_diff": 3,
            "mini_len": 5
        }, "rmq": {
            "activate": True,
            "window": 20,
            "rank": 5
        }, "manual": {
            "activate": False,
        }, "file": {
            "activate": False,
            "location": "pos.txt"
        }
    }, "show_spectrum": {
        "rank": 3,
        "execute": True
    }, "global": {
        "x": {
            "row": 1,
            "column": 0
        }, "y": {
            "row": 1,
            "column": 4
        }, "rows": {
            "value": 150,
            "always_request": False  # Not implemented
        }, "show_rerun": True  # Not implemented
    }
}


def read_config():
    global config
    with open(config_path, "r") as f:
        conf = ""
        tmp = f.read()
        while tmp != "":
            tmp = f.read()
            conf += tmp
        config = json.load(conf)


def config_not_exist():
    print("Config file does not exist ,use default config.")


fname = input("Input the folder name(as batch) or input the file name(as single):")
files = []
if '.' in fname:  # regard as a folder
    parent = os.path.abspath(fname)
    files = [fname]
    while parent[len(parent) - 1] != "\\":
        parent = parent[:len(parent) - 1]
    if os.path.exists(parent + "config.json"):
        read_config()
    else:
        config_not_exist()
else:
    fname = os.path.abspath(fname)
    config_path = fname + "/config.json"
    if os.path.exists(config_path):
        read_config()
    else:
        config_not_exist()
    files = glob.glob(fname + "/*.csv")

if config["show_envelope"]["execute"]:
    show_envelope(files, config)
if config["show_spectrum"]["execute"]:
    spectrum(files, config)
