# CtrlTerm.py
# Class to define content of the Terminal tab.
#
# Change history:
#   20191115:KDT - Original issue

# CtrlConfig.py
# Class to define content of the config tab.
#
# Change history:
#   20191115:KDT - Original issue

from tkinter import Frame, LabelFrame, Label, Spinbox, Text, Entry

import tkinter as tk

import Data_coord

LARGE_FONT = ("Verdana", 12)


class CtrlTerm(Frame) :
    def __init__(self, parent, g_sys_instance, cons, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.g_sys_instance = g_sys_instance
        self.cons = cons
        self.buildContent()

    def buildContent(self) :

        self.input_text = Text(self, borderwidth=0)

        self.input_text.pack(fill=tk.BOTH)

        self.input_text.bind("<Return>", self.send_command)


    def send_command(self, event):

        #parsing the terminal command into a cmd and a parm needs to happen here 

        command = self.input_text.get(1.0,'end-1c') 

        reply = self.cons.send_command_to_PC(command)

        self.input_text.insert(tk.END,'\n'+reply)