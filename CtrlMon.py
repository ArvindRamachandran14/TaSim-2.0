# CtrlMon.py
# Class to define content of the Monitor tab.
#
# Change history:
#   20191115:KDT - Original issue

import tkinter as tk 
from tkinter import ttk, Frame, Canvas, LabelFrame, Label, Spinbox, OptionMenu, StringVar
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # , NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import global_var as gv

class CtrlMon(Frame) :
    def __init__(self, name, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.buildContent()

    def buildContent(self) :

        variable_temp = StringVar(self)
        variable_temp.set("Sample Chamber")

        variable_pressure = StringVar(self)
        variable_pressure.set("pCO2")


        self.temp_select = LabelFrame(self, text = ' Temperatures (' + chr(176) + 'C)')
        self.temp_select.grid(row=0,column=0, padx=10, pady=10)
        self.label1 = Label(self.temp_select, text = 'Choose Temperature')
        self.label1.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')
        self.menu1 = OptionMenu(self.temp_select, variable_temp, "Sample Chamber", "Conditioning Chamber", "Dew Point Generator")
        self.menu1.grid(row = 1, column = 0, padx = 2, pady = 2, sticky='w')
       
        self.pressure_select = LabelFrame(self, text = ' Partial Pressure (ppm) ')
        self.pressure_select.grid(row=0,column=1, padx=10, pady=10)
        self.label2 = Label(self.pressure_select, text = 'Choose pressure')
        self.label2.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')
        self.menu2 = OptionMenu(self.pressure_select, variable_pressure, "pCO2", "pH2O")
        self.menu2.grid(row = 1, column = 0, padx = 2, pady = 2, sticky='w')

        self.scale = LabelFrame(self, text = 'Sample weight (g)')
        self.scale.grid(row=0,column=2, padx=10, pady=10)
        self.label3 = Label(self.scale, text = 'Sample weight')
        self.label3.grid(row = 0, column = 0, padx = 3, pady = 3, sticky='e')

        # Temperatures and humidity
        self.grpTemps = LabelFrame(self, text = ' Temperatures and Humidity ')
        self.grpTemps.grid(row=1,column=0, padx=5, pady=5)

        #self.grpTemps.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.fig1 = Figure(figsize=(3.8, 3.8))
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_xlabel('Time (min)')
        self.ax1.set_ylabel('Temperature ($^\circ$C)')
        self.ax1.set_autoscalex_on(True)
        #self.ax1.set_ybound(0, 50)
        self.ax1.set_autoscaley_on(False)
        self.ax1.grid(True, 'major', 'both')
        self.fig1.tight_layout()
        self.cnvs1 = FigureCanvasTkAgg(self.fig1, self.grpTemps)
        self.cnvs1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
      
        # Partial pressures
        self.grpPps = LabelFrame(self, text = ' Partial pressures ')
        self.grpPps.grid(row=1,column=1, padx=5, pady=5)
        self.fig2 = Figure(figsize=(3.8, 3.8))
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_xlabel('Time (min)')
        self.ax2.set_ylabel('pH20/pCO2 (Pa)')
        self.ax2.set_autoscalex_on(True)
        self.ax2.set_ybound(0, 10000)
        self.ax2.set_autoscaley_on(False)
        self.ax2.grid(True, 'major', 'both')
        #plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.fig2.tight_layout()
        self.cnvs2 = FigureCanvasTkAgg(self.fig2, self.grpPps)
        self.cnvs2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Sample weight
        self.grpSWgt = LabelFrame(self, text = ' Sample Weight ')
        self.grpSWgt.grid(row=1,column=2, padx=5, pady=5)
        self.fig3 = Figure(figsize=(3.8, 3.8))
        self.ax3 = self.fig3.add_subplot(111)
        self.ax3.set_xlabel('Time (min)')
        self.ax3.set_ylabel('Weight (g)')
        self.ax3.set_autoscalex_on(True)
        self.ax3.set_ybound(0, 10)
        self.ax3.set_autoscaley_on(False)
        self.ax3.grid(True, 'major', 'both')
        self.fig3.tight_layout()
        self.cnvs3 = FigureCanvasTkAgg(self.fig3, self.grpSWgt)
        self.cnvs3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def animate_SC(self, i):

        print('Time', gv.time_list)
        print('Temperature', gv.Temperatures_SC)

        #self.ax1.clear()

        self.ax1.plot(gv.time_list, gv.Temperatures_SC)
