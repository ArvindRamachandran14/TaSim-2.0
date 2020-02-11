# globals.py
# Globals as needed
# Change history:
#   20191112:KDT - Original issue

# Global variables

import json

cfgFile = 'taui.json'
mainForm = None
cfg = {}                        # Config object
tty = None                      # TTY or COM port to use for TA comms

# initialize
# Initialize globals from the cfg object
def initialize(config) :
    global cfg, tty, baud_rate, time_out, time_interval, ser
    cfg = config                            # Set the cfg
    tty = cfg["tty"]
    baud_rate = cfg["baud_rate"]
    time_out = cfg["time_out"]
    time_interval = cfg["time_interval"]


def update():

    cfg["tty"] = tty

    cfg["baud_rate"] = baud_rate

    cfg["time_out"] = time_out

    cfg["time_interval"] = time_interval

    print(cfg)

    with open(cfgFile, 'w') as fCfg:

        json.dump(cfg, fCfg)