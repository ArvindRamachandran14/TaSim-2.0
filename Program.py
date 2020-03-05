# Program.py
# Program to implement the User Interface.  This is the startkup program.
# It sets up the environment and starts the main application.

import tkinter as tk 
import sys
import json
import globals as g
import matplotlib.animation as animation
import CtrlMon
import global_var as gv
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
    
    g_instance = g.globals()              # Initialize the globals

    #g_instance.update()

    gv_instance = gv.globals()

    cons = Data_coord.consumer(2, g_instance, gv_instance)

    mainForm = MainForm(g_instance, gv_instance, cons)

    ani_SC = animation.FuncAnimation(g_instance.mainForm.tabMon.fig1, g_instance.mainForm.tabMon.animate_SC, interval=1000)

    def apploop():
    
        if g_instance.bconnected == "True":
    
            print('Consumption in progress')

            cons.consume()

        mainForm.after(2000, apploop)

    apploop()

    mainForm.mainloop()

# Actual main program


main(sys.argv)
