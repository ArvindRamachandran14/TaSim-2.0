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
import global_sys_var as g_sys
import Data_coord

class CtrlMon(Frame) :
    def __init__(self, name, g_sys_instance, *args, **kwargs) :
       
        Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.g_sys_instance = g_sys_instance
        self.buildContent()

    def buildContent(self) :

        variable_temp = StringVar(self)
        variable_temp.set("Sample Chamber")

        variable_pressure = StringVar(self)
        variable_pressure.set("pCO2")

        self.label1 = Label(self, text = 'Sample Chamber Temperature')
        self.label1.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')
  
        self.label2 = Label(self, text = 'Conditioning Chamber Temperature')
        self.label2.grid(row = 0, column = 1, padx = 2, pady = 2, sticky='e')
  
        self.label3 = Label(self, text = 'Dew Point Generator Temperatures')
        self.label3.grid(row = 0, column = 2, padx = 3, pady = 3, sticky='e')

        self.fig1 = Figure(figsize=(3.8, 3.8))
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_xlabel('Time (sec)')
        self.ax1.set_ylabel('Temperature ($^\circ$C)')
        self.ax1.set_autoscalex_on(True)
        #self.ax1.set_ybound(0, 50)
        self.ax1.set_autoscaley_on(True)
        self.ax1.grid(True, 'major', 'both')
        self.fig1.tight_layout()
        self.cnvs1 = FigureCanvasTkAgg(self.fig1, self)
        self.cnvs1.get_tk_widget().grid(row=1, column=0)
        #self.cnvs1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
      
        # Conditioning Chamber temperature

        self.fig2 = Figure(figsize=(3.8, 3.8))
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_xlabel('Time (sec)')
        self.ax2.set_ylabel('Temperature ($^\circ$C)')
        self.ax2.set_autoscalex_on(True)
        #self.ax1.set_ybound(0, 50)
        self.ax2.set_autoscaley_on(True)
        self.ax2.grid(True, 'major', 'both')
        self.fig2.tight_layout()
        self.cnvs2 = FigureCanvasTkAgg(self.fig2, self)
        self.cnvs2.get_tk_widget().grid(row=1, column=1)
        #self.cnvs2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Sample weight
        self.fig3 = Figure(figsize=(3.8, 3.8))
        self.ax3 = self.fig3.add_subplot(111)
        self.ax3.set_xlabel('Time (sec)')
        self.ax3.set_ylabel('Temperature ($^\circ$C)')
        self.ax3.set_autoscalex_on(True)
        #self.ax1.set_ybound(0, 50)
        self.ax3.set_autoscaley_on(True)
        self.ax3.grid(True, 'major', 'both')
        self.fig3.tight_layout()
        self.cnvs3 = FigureCanvasTkAgg(self.fig3, self)
        self.cnvs3.get_tk_widget().grid(row=1, column=2)
        #self.cnvs3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    def animate_SC(self, i):

        self.ax1.plot(self.g_sys_instance.time_list, self.g_sys_instance.Temperatures_SC)

    def animate_CC(self, i):

        self.ax2.plot(self.g_sys_instance.time_list, self.g_sys_instance.Temperatures_SC)

    def animate_DPG(self, i):

        self.ax3.plot(self.g_sys_instance.time_list, self.g_sys_instanceTemperatures_DPG)
