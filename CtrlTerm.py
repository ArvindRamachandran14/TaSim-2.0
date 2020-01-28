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

LARGE_FONT = ("Verdana", 12)


class CtrlTerm(Frame) :
    def __init__(self, parent, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.buildContent()

    def buildContent(self) :

        self.input_text = Text(self, borderwidth=0)

        self.input_text.pack(fill=tk.BOTH)

        self.input_text.bind("<Return>", self.send_command)


    def send_command(self, event):

        #parsing the terminal command into a cmd and a parm needs to happen here 

        mainform.cmd = self.input_text.get(1.0,'end-1c') 

        self.input_text.insert(tk.END,'\n'+self.input_text.get(1.0,'end-1c'))

        