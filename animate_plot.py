
########################################## Tkinter modules ##########################################

import tkinter as tk 

from tkinter import ttk # For more aesthetic buttons

########################################## Matplotlib modules ##########################################

import matplotlib 

#import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.figure import Figure

import matplotlib.animation as animation

from matplotlib import style

########################################## Time/Datetime modules ##################################

import time

from datetime import datetime

########################################## Other modules ##########################################


import numpy as np

import random

import serial

matplotlib.use("TkAgg") 

style.use("ggplot")

LARGE_FONT = ("Verdana", 12)

Time_SC = []

Time_in_seconds_SC = []

Time_in_minutes_SC = []

Temperatures_SC = []

LARGE_FONT = ("Verdana", 12)

f_SC = Figure(figsize=(5,5), dpi=100) 

a_SC = f_SC.add_subplot(111) # 1 by 1 and this is plot number 1


def animate_SC(i): 

    #Function used to create live plot of Temperature vs Time in seconds 

    Time_SC_temp = datetime.now()

    Time_SC.append(Time_SC_temp)

    Time_in_seconds_SC_temp = (Time_SC[-1]-Time_SC[0]).seconds

    Time_in_seconds_SC.append(Time_in_seconds_SC_temp)

    Time_in_minutes_SC_temp = Time_in_seconds_SC_temp/60.0

    Time_in_minutes_SC.append(Time_in_minutes_SC_temp)

    Temperatures_SC_temp = float(random.randint(10, 100)/100.0)

    Temperatures_SC.append(Temperatures_SC_temp)

    #a_SC.clear()

    a_SC.plot(Time_in_minutes_SC, Temperatures_SC)

    #plt.show()

def animate_plot():

    ani_SC = animation.FuncAnimation(f_SC, animate_SC, interval=1000)


class main_window(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self)

        tk.Tk.wm_title(self, "Graphics_window" )

        container = tk.Frame(self) 

        container.pack()

        self.minsize(height = 700, width = 1024)

        container.grid_rowconfigure(0, weight=1) #0 is minimum size. weight is a priortity metric, in this case rows and columns have equal priority

        container.grid_columnconfigure(0, weight=1)

        canvas = FigureCanvasTkAgg(f_SC, container)

        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, container)

        toolbar.update()

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True) 

        self.btn_text = tk.StringVar()

        self.button1 = tk.Button(container, textvariable=self.btn_text)

        self.btn_text.set('Connect')

        self.button1.pack()


def plot_live_SC_data(controller): 

    global Time_in_seconds_SC_temp ,  Time_in_minutes_SC, Temperatures_SC

    Time_SC_temp = datetime.now()

    Time_SC.append(Time_SC_temp)

    Time_in_seconds_SC_temp = (Time_SC[-1]-Time_SC[0]).seconds

    Time_in_seconds_SC.append(Time_in_seconds_SC_temp)

    Time_in_minutes_SC_temp = Time_in_seconds_SC_temp/60.0

    Time_in_minutes_SC.append(Time_in_minutes_SC_temp)

    Temperatures_SC_temp = float(random.randint(10, 100)/100.0)

    Temperatures_SC.append(Temperatures_SC_temp)

    controller.after(1000, plot_live_SC_data, controller)     

root = main_window()

#ani_SC = animation.FuncAnimation(f_SC, animate_SC, interval=1000)

animate_plot()

root.mainloop()
