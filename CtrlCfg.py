# -*- coding: utf-8 -*-
# CtrlCfg.py
# Class to define content of the Config tab.
#
# Change history:
#   20191115:KDT - Original issue

from tkinter import Frame, LabelFrame, Label, Spinbox, StringVar, Button, Entry

import json

class CtrlCfg(Frame) :
    def __init__(self, name, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.btn_text = StringVar()
        self.buildContent()

    def buildContent(self) :

        self.label = Label(self, text="Enter interval")

        self.label.grid(row=0,column=0) 

        self.interval = StringVar()

        self.entry = Entry(self, textvariable=self.interval)
        
        self.interval.set('5')      

        self.entry.grid(row=0, column=1)

        self.entry.bind("<Enter>", self.update_json_file)


    def update_json_file(self, event):

        g.time_interval = self.interval.get()

        g.update()
