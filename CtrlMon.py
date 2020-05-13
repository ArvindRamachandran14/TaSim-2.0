# CtrlMon.py
# Class to define content of the Monitor tab.
#
# Change history:
#   20191115:KDT - Original issue

import tkinter as tk 
from tkinter import ttk, Frame, Canvas, LabelFrame, Label, Spinbox, OptionMenu, StringVar, Button, Scale, HORIZONTAL, VERTICAL
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import global_sys_var as g_sys
import Data_coord

class CtrlMon(Frame) :
    def __init__(self, name, g_sys_instance, consumer_object, mainform_object, *args, **kwargs) :
       
        Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.g_sys_instance = g_sys_instance
        self.consumer_object = consumer_object
        self.mainform_object = mainform_object
        self.log_btn_text = StringVar()
        self.exp_btn_text = StringVar()
        self.log_btn_text.set('Record data')
        self.exp_btn_text.set('Start experiment')
        self.plot1_range = 7 #7 data points leads to 15 second data
        self.plot2_range = 7 
        self.plot3_range = 7 
        self.slider_list = [1, 15, 30, 60]
        self.buildContent()

    def buildContent(self) :

        self.label = Label(self, text ="")

        self.label.grid(row=0, column=0, rowspan=2)

        self.button1 = ttk.Button(self, textvariable=self.exp_btn_text, command=self.run_experiment)
        self.button1.grid(row=2, column=0, columnspan=2)

        self.button2 = ttk.Button(self, textvariable=self.log_btn_text, command=self.log_data)
        self.button2.grid(row=2, column=1, columnspan=2)

        self.label = Label(self, text ="")

        self.label.grid(row=3, column=0, rowspan=2)

        self.label1 = Label(self, text = 'Sample Chamber Temperature')
        self.label1.grid(row = 5, column = 0, padx = 2, pady = 2)
  
        self.label2 = Label(self, text = 'Conditioning Chamber Temperature')
        self.label2.grid(row = 5, column = 1, padx = 2, pady = 2)
  
        self.label3 = Label(self, text = 'Dew Point Generator Temperatures')
        self.label3.grid(row = 5, column = 2, padx = 3, pady = 3)

        self.toolbarframe1 = Frame(self)

        self.toolbarframe2 = Frame(self)

        self.toolbarframe3 = Frame(self)

        self.scale1 = Scale(self, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_value_check1, orient=HORIZONTAL, label='Plot range (m)')#, command=set_plot_range(1))
        self.scale1.grid(row=6, column=0, rowspan=1)

        self.scale2 = Scale(self, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_value_check2, orient=HORIZONTAL, label='Plot range (m)')#, command=set_plot_range(2))
        self.scale2.grid(row=6, column=1, rowspan=1)

        self.scale3 = Scale(self, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_value_check3, orient=HORIZONTAL, label='Plot range (m)')#, command=set_plot_range(3))
        self.scale3.grid(row=6, column=2, rowspan=1)

        # Plot Sample Chamber temperature

        self.fig1 = Figure(figsize=(3.8, 3.8))
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_xlabel('Time (sec)')
        self.ax1.set_ylabel('Temperature ($^\circ$C)')
        self.ax1.set_autoscalex_on(True)
        self.ax1.set_ybound(10, 40)
        self.ax1.set_autoscaley_on(False)
        self.ax1.grid(True, 'major', 'both')
        self.fig1.tight_layout()
      
        self.cnvs1 = FigureCanvasTkAgg(self.fig1, self)
        self.cnvs1.get_tk_widget().grid(row=7, column=0)

        #self.toolbarframe1.grid(row=8, column=0)

        #self.toolbar1 = NavigationToolbar2Tk(self.cnvs1,self.toolbarframe1)
       
        #self.cnvs1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
      
        #Plot Conditioning Chamber temperature

        self.fig2 = Figure(figsize=(3.8, 3.8))
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_xlabel('Time (sec)')
        self.ax2.set_ylabel('Temperature ($^\circ$C)')
        self.ax2.set_autoscalex_on(True)
        self.ax2.set_ybound(10, 40)
        self.ax2.set_autoscaley_on(False)
        self.ax2.grid(True, 'major', 'both')
        self.fig2.tight_layout()
   
        self.cnvs2 = FigureCanvasTkAgg(self.fig2, self)
        self.cnvs2.get_tk_widget().grid(row=7, column=1)

        #self.toolbarframe2.grid(row=8, column=1)

        #self.toolbar2 = NavigationToolbar2Tk(self.cnvs2,self.toolbarframe2)

       
        #self.cnvs2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Plot DPG temperature

        self.fig3 = Figure(figsize=(3.8, 3.8))
        self.ax3 = self.fig3.add_subplot(111)
        self.ax3.set_xlabel('Time (sec)')
        self.ax3.set_ylabel('Temperature ($^\circ$C)')
        self.ax3.set_autoscalex_on(True)
        self.ax3.set_ybound(10, 40)
        self.ax3.set_autoscaley_on(False)
        self.ax3.grid(True, 'major', 'both')
        self.fig3.tight_layout()
   
        self.cnvs3 = FigureCanvasTkAgg(self.fig3, self)
        self.cnvs3.get_tk_widget().grid(row=7, column=2)

        #self.toolbarframe3.grid(row=8, column=2)

        #self.toolbar3 = NavigationToolbar2Tk(self.cnvs3,self.toolbarframe3)


       
        #self.cnvs3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    '''
    def set_plot_range(graph_no):

        if graph_no == 1:

            self.plot1_range = self.scale1.get()

        elif graph_no == 2:

            self.plot2_range = self.scale2.get()

         elif graph_no == 3:

            self.plot3_range = self.scale3.get()
    '''

    def scale_value_check1(self, value):

        newvalue = min(self.slider_list, key=lambda x:abs(x-float(value)))
       
        self.scale1.set(newvalue)

    def scale_value_check2(self, value):

        newvalue = min(self.slider_list, key=lambda x:abs(x-float(value)))
       
        self.scale2.set(newvalue)

    def scale_value_check3(self, value):

        newvalue = min(self.slider_list, key=lambda x:abs(x-float(value)))
       
        self.scale3.set(newvalue)


    def animate_SC(self, i):

        self.ax1.clear()
        self.ax1.set_xlabel('Time (sec)')
        self.ax1.set_ylabel('Temperature ($^\circ$C)')
        self.ax1.set_autoscalex_on(True)
        self.ax1.set_ybound(10, 40)
        self.ax1.set_autoscaley_on(False)
        self.ax1.grid(True, 'major', 'both')

        plot_range = self.scale1.get()*60 #converting seconds to list range

        #print('range type', type(range))

        index = int(plot_range/15.0)

        self.ax1.plot(self.g_sys_instance.time_list[(10000-self.plot1_range*index)::index], self.g_sys_instance.Temperatures_SC[(10000-self.plot1_range*index)::index], 'k')

    def animate_CC(self, i):

        self.ax2.clear()

        self.ax2.set_xlabel('Time (sec)')
        self.ax2.set_ylabel('Temperature ($^\circ$C)')
        self.ax2.set_autoscalex_on(True)
        self.ax2.set_ybound(10, 40)
        self.ax2.set_autoscaley_on(False)
        self.ax2.grid(True, 'major', 'both')


        plot_range = self.scale2.get()*60 #converting seconds to list range

        index = int(plot_range/15.0)

        self.ax2.plot(self.g_sys_instance.time_list[(10000-self.plot2_range*index)::index], self.g_sys_instance.Temperatures_CC[(10000-self.plot2_range*index)::index], 'k')

    def animate_DPG(self, i):

        self.ax3.clear()

        self.ax3.set_xlabel('Time (sec)')
        self.ax3.set_ylabel('Temperature ($^\circ$C)')
        self.ax3.set_autoscalex_on(True)
        self.ax3.set_ybound(10, 40)
        self.ax3.set_autoscaley_on(False)
        self.ax3.grid(True, 'major', 'both')

        plot_range = self.scale3.get()*60 #converting seconds to list range

        index = int(plot_range/15.0)

        self.ax3.plot(self.g_sys_instance.time_list[(10000-self.plot3_range*index)::index], self.g_sys_instance.Temperatures_DPG[(10000-self.plot3_range*index)::index], 'k')

    def run_experiment(self):

        if str(self.exp_btn_text.get()) == "Start experiment":

            self.g_sys_instance.run_experiment = True

            self.exp_btn_text.set('Stop experiment')

            self.mainform_object.status_label_text.set('Running')

        elif str(self.exp_btn_text.get()) == 'Stop experiment':

            self.g_sys_instance.run_experiment = False

            self.exp_btn_text.set('Start experiment')

            self.mainform_object.status_label_text.set('Idle')


    def log_data(self):

        #print(self.log_btn_text.get())

        if str(self.log_btn_text.get()) == "Record data": 

            self.consumer_object.log_data(self) 

        elif str(self.log_btn_text.get()) == 'Stop recording':

            self.consumer_object.stop_logging()

            self.log_btn_text.set('Record data') 
