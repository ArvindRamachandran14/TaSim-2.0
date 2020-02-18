# Program.py
# Program to implement the User Interface.  This is the startkup program.
# It sets up the environment and starts the main application.

import tkinter as tk 
import sys
import json
import globals as g
import matplotlib.animation as animation
import CtrlMon

from MainForm import MainForm

def main(argv) :
    idx = 1
    option = None
    while idx < len(argv) :
        if argv[idx] == 'option' :
            if idx + 1 < len(argv) :
                idx += 1
                option = argv[idx]
        idx += 1

    if not option == None :
        print(option)

    with open(g.cfgFile, 'r') as fCfg :
        config = json.loads(fCfg.read())        # Read config file
        g.initialize(config)              # Initialize the globals

    CtrlMon_object = CtrlMon.CtrlMon()

    # Start the mainform
    g.mainForm = MainForm()

    CtrlMon_object.animate(CtrlMon_object.fig1, CtrlMon_object.animate_SC, interval=1000)

    g.mainForm.mainloop()

# Actual main program
main(sys.argv)






