# CtrlCfg.py
# Class to define content of the Config tab.
#
# Change history:
#   20191115:KDT - Original issue

from tkinter import Frame, LabelFrame, Label, Spinbox, StringVar, Button, Entry

import globals as g

class CtrlCfg(Frame) :
    def __init__(self, name, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.btn_text = StringVar()
        self.buildContent()

    def buildContent(self) :

        self.label = Label(self, text="Enter interval")

        self.label.grid(row=0,column=0)

        self.entry = Entry(self, command=self.update_json_file)

        self.entry.grid(row=0, column=1)


    def update_json_file(self, event):

        g.time_interval = self.entry.get()

        g.update()