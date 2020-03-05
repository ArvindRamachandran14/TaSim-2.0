# globals.pyxw
# Globals as needed
# Change history:
#   20191112:KDT - Original issue

# Global variables

import json

class globals():

    def __init_(self, config) :
        self.mainForm = None
        self.cfgFile = 'taui.json'
        self.cfg = config                            # Set the cfg
        self.tty = self.cfg["tty"]
        self.baud_rate = self.cfg["baud_rate"]
        self.time_out = self.cfg["time_out"]
        self.time_interval = self.cfg["time_interval"]
        self.bconnected = "False"

    def update():

        self.cfg["tty"] = self.tty

        self.cfg["baud_rate"] = self.baud_rate

        self.cfg["time_out"] = self.time_out

        self.cfg["time_interval"] = self.time_interval

        self.cfg["bconnected"] = self.bconnected

        print(self.cfg)

        with open(self.cfgFile, 'w') as fCfg:

            json.dump(self.cfg, fCfg)
