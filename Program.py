# Program.py
# Program to implement the User Interface.  This is the startkup program.
# It sets up the environment and starts the main application.

import tkinter as tk 
import sys
import json
import global_tech_var as g_tech_instance
import matplotlib.animation as animation
import CtrlMon
import global_sys_var as g_sys
import Data_coord


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

        # Read config file
    
    #g_tech_instance = g_tech.globals_()              # Initialize the globals

    g_sys_instance = g_sys.globals_()

    cons = Data_coord.consumer(2, g_sys_instance)

    mainForm = MainForm(g_sys_instance, cons)

    ani_SC = animation.FuncAnimation(mainForm.tabMon.fig1, mainForm.tabMon.animate_SC, interval=1000)

    def apploop():

        with open('taui.json', 'r') as fCfg :
            
            config = json.loads(fCfg.read())

            bconnected = config["bconnected"]
        
        if bconnected == "True":
    
            #print('Consumption in progress')

            cons.consume()

        mainForm.after(2000, apploop)

    apploop()

    mainForm.mainloop()

# Actual main program


main(sys.argv)
