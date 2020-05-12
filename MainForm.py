# -*- coding: utf-8 -*-
# Mainform.py
# Build the main form.
# This is the topleel of the GUI tree.
#
# 20191112: KDT = Original issue

import tkinter as tk
from tkinter import Tk, ttk, Frame, Menu, Menubutton, Button, Label, StringVar, OptionMenu
import sys
from datetime import datetime
import CtrlSetup
import CtrlMon
import CtrlMon2
import global_tech_var as g_tech_instance
import CtrlTerm
import CtrlCfg
import serial
import time
#import TADAQ
import Data_coord
import json

class MainForm(Tk) :
    
    def __init__(self, g_sys_instance, cons, *args, **kwargs) :
        
        # self.bconnected = False

        tk.Tk.__init__(self, *args, **kwargs) 


        tk.Tk.wm_title(self, 'Main Window') #window title

        self.grid_rowconfigure(0, weight=1)  #Let the window fill out when resizing
        self.grid_columnconfigure(0, weight=1)  #Let the window fill out when resizing

        container = tk.Frame(self) #main frame
        
        container.grid(row=0, column=0, sticky=tk.E+tk.W+tk.S+tk.N) # Let the main frame fill out the entire window

        container.grid_rowconfigure(1, weight=1) # Notebook sits in row 1 and it should occupy any empty space left
        container.grid_columnconfigure(0, weight=1) # Makes sure there is no empty space in the horizontal direction

        self.g_sys_instance = g_sys_instance
        self.cons = cons

        self.minsize(height = 700, width = 1024) # setting window size
        self.protocol("WM_DELETE_WINDOW", self.onClosing) 
        self.btn_text = StringVar()
        self.buildMenuBar(container)
        self.buildserialBar(container)
        self.buildCtrlTab(container)
        self.buildStatusBar(container)
        self.ctrlTab.select(self.tabSetup)
        self.dat_buf = []

        #self.dcoord = DCoord(Rec_num) # This is renaming the consumer class 

        #self.cmd = ''

        #self.parm = ''

    def buildMenuBar(self, container) :
        # Menu
        menuBar = tk.Menu(container)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label='Mew', command=self.onFileNew)
        fileMenu.add_command(label='Open...', command=self.onFileOpen)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self.onFileExit)
        menuBar.add_cascade(label='File', menu=fileMenu)
        tk.Tk.config(self, menu = menuBar)

    #Build serial bar - lets the user choose the serial port, baud rate and establish connection through a "connect" button


    def buildserialBar(self, container):

        serial_port = StringVar()

        baud_rate = StringVar()

        self.serialBar = tk.Frame(container, relief=tk.SUNKEN)

        self.serialBar.grid(row=0, column=0) # Serial bar is positioned at the top row of the frame

        self.serial_port_label = Label(self.serialBar, text="Port") 

        self.serial_port_label.grid(row=0, column=0)

        tty_list = ["/dev/ttyUSB0", "/dev/ttyUSB1"]

        self.tty_variable = StringVar()

        self.tty_variable.set(g_tech_instance.tty)

        self.serial_port_list = OptionMenu(self.serialBar, self.tty_variable, *tty_list, command=self.update_json_file)

        self.serial_port_list.grid(row=0, column=1)

        self.baud_rate_label = Label(self.serialBar, text="Baud")

        self.baud_rate_label.grid(row=0, column=2)

        baud_rate_list = ["9600", "19200", "115200"]

        self.baud_rate_variable = StringVar()

        self.baud_rate_variable.set(g_tech_instance.baud_rate)

        self.baud_rate_list = OptionMenu(self.serialBar, self.baud_rate_variable, *baud_rate_list, command=self.update_json_file)

        self.baud_rate_list.grid(row=0, column=3)        

        self.button = Button(self.serialBar, textvariable=self.btn_text, command=self.connect)
        
        self.btn_text.set("Connect")

        print(self.btn_text.get())

        self.button.grid(row=0, column=4)


    # buildStatusBar
    # Make the status bar on the bottom of the screen.  This has
    # a text status message on the left and the experiment time on
    # the right.  The time is not being updated in this prototype code.

    def buildStatusBar(self, container) :
        statusBar = tk.Frame(container, relief=tk.SUNKEN, bd=2)

        statusBar.grid(row=2, column=0, sticky=tk.E+tk.W) #Status bar is positioned at the bottom and extends fully horizontally
 
        tk.Label(statusBar, text='Idle').pack(side=tk.LEFT)

        tk.Label(statusBar, text='Time').pack(side=tk.RIGHT)


    def buildCtrlTab(self, container) :
        
        ################# Hosts the different tabs such as SetUp, Monitor, Terminal, and Config #################
        
        self.ctrlTab = ttk.Notebook(container)
        self.tabSetup = CtrlSetup.CtrlSetup(self.ctrlTab, self.cons)
        self.ctrlTab.add(self.tabSetup, text = 'Setup')
        self.tabMon = CtrlMon.CtrlMon(self.ctrlTab, self.g_sys_instance, self.cons, self)
        self.tabMon2 = CtrlMon2.CtrlMon2(self.ctrlTab, self.g_sys_instance)

        self.ctrlTab.add(self.tabMon, text = 'Monitor 1')

        self.ctrlTab.add(self.tabMon2, text = 'Monitor 2')

        self.tabTerm = CtrlTerm.CtrlTerm(self.ctrlTab, self.g_sys_instance, self.cons)
        self.ctrlTab.add(self.tabTerm, text = 'Terminal')
        self.tabCfg = CtrlCfg.CtrlCfg(self.ctrlTab)
        self.ctrlTab.add(self.tabCfg, text = 'Config')
        self.ctrlTab.grid(row=1, column=0,sticky=tk.E+tk.W+tk.S+tk.N)

    def update_json_file(self, event):

        #### Gets the updated serial port and baud rate and alls the function to update the json file with the latest parameters ####

        g_tech_instance.baud_rate = self.baud_rate_variable.get()

        g_tech_instance.tty = self.tty_variable.get()

        g_tech_instance.update()

    def connect(self):

        time_out = 3

        if str(self.btn_text.get()) == "Connect":

           self.cons.Connect(self, str(time_out)) #TAD_rec_count is the total number of record
        
        elif str(self.btn_text.get()) == "Disconnect":

            self.cons.Disconnect()

            self.btn_text.set("Connect")

        time.sleep(4)

        if g_tech_instance.bconnected == "True":# Check for connection via global connection flag

            #print('Connected')

            self.btn_text.set("Disconnect") #Update "connect" button to "disconnect" 
           
    def onFileNew(self) :
        popupmsg("Not Implemented")

    def onFileOpen(self) :
        popupmsg("Not Implemented")

    def onFileExit(self) :
        # Need to do cleanup here, save files, etc. before quitting.
        quit()

    def onClosing(self) :
        self.onFileExit()

    def machineloop():

        if self.bconnected:

            if self.cmd != '':

                self.cmd = '$GET'

                self.parm = 'ALL_DATA'

            bok, dat_buf = self.conns.submit(self.cmd, self.parm)

            self.cmd = ''

            self.parm = ''

            if bok:

                pass

                # To do: Do something dat_buf to update widgets

                #: Update the forms - monitor, set up etc..

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Information")
    label = ttk.Label(popup, text=msg)
    #label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    #B1.pack()
    popup.mainloop()
