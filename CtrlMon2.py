# CtrlMon2.py
# Class to define content of the Monitor 2 tab.
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

class CtrlMon2(Frame) :
    def __init__(self, name, g_sys_instance, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.g_sys_instance = g_sys_instance
        self.buildContent()

    def buildContent(self) :

        self.grp1 = LabelFrame(self, text = 'Partial pressure of CO2')
        self.grp1.grid(row=1,column=1, padx=5, pady=5)
        self.fig1 = Figure(figsize=(3.8, 3.8))
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_xlabel('Time (min)')
        self.ax1.set_ylabel('pCO2 (Pa)')
        self.ax1.set_autoscalex_on(True)
        self.ax1.set_ybound(0, 10000)
        self.ax1.set_autoscaley_on(False)
        self.ax1.grid(True, 'major', 'both')
        #plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.fig1.tight_layout()
        self.cnvs1 = FigureCanvasTkAgg(self.fig1, self.grp1)
        self.cnvs1.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Partial pressures
        self.grp2 = LabelFrame(self, text = 'Partial pressure of H2O')
        self.grp2.grid(row=1,column=1, padx=5, pady=5)
        self.fig2 = Figure(figsize=(3.8, 3.8))
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_xlabel('Time (min)')
        self.ax2.set_ylabel('pH20 (Pa)')
        self.ax2.set_autoscalex_on(True)
        self.ax2.set_ybound(0, 10000)
        self.ax2.set_autoscaley_on(False)
        self.ax2.grid(True, 'major', 'both')
        #plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.fig2.tight_layout()
        self.cnvs2 = FigureCanvasTkAgg(self.fig2, self.grp2)
        self.cnvs2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Sample weight
        self.grp3 = LabelFrame(self, text = 'Sample Weight')
        self.grp3.grid(row=1,column=2, padx=5, pady=5)
        self.fig3 = Figure(figsize=(3.8, 3.8))
        self.ax3 = self.fig3.add_subplot(111)
        self.ax3.set_xlabel('Time (min)')
        self.ax3.set_ylabel('Weight (g)')
        self.ax3.set_autoscalex_on(True)
        self.ax3.set_ybound(0, 10)
        self.ax3.set_autoscaley_on(False)
        self.ax3.grid(True, 'major', 'both')
        self.fig3.tight_layout()
        self.cnvs3 = FigureCanvasTkAgg(self.fig3, self.grp3)
        self.cnvs3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def animate_pCO2(self, i):

        self.ax1.plot(self.g_sys_instance.time_list, self.g_sys_instance.pCO2_list)


    def animate_pH2O(self, i):

        self.ax2.plot(self.g_sys_instance.time_list, self.g_sys_instance.pH2O_list)


    def animate_sw(self, i):

        self.ax3.plot(self.g_sys_instance.time_list, self.g_sys_instance.sample_weight)





