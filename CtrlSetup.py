# CtrlConfig.py
# Class to define content of the config tab.
#
# Change history:
#   20191115:KDT - Original issue

from tkinter import Frame, LabelFrame, Label, Spinbox 

class CtrlSetup(Frame) :
    def __init__(self, parent, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.buildContent()

    def buildContent(self) :
        self.grpSetpoint = LabelFrame(self, text = ' Setpoints ')
        self.grpSetpoint.grid(row=0,column=0, padx=10, pady=10)
        self.label1 = Label(self.grpSetpoint, text = 'Sample Chamber T (' +chr(176) + 'C):')
        self.label1.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb1 = Spinbox(self.grpSetpoint, from_ = 5, to_ = 50, width = 5)
        self.sb1.grid(row = 0, column = 1, padx = 2, pady = 2, sticky='w')
        self.label2 = Label(self.grpSetpoint, text = 'Conditioning Chamber T (' +chr(176) + 'C):')
        self.label2.grid(row = 1, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb2 = Spinbox(self.grpSetpoint, from_ = 5, to_ = 50, width = 5)
        self.sb2.grid(row = 1, column = 1, padx = 2, pady = 2, sticky='w')
        self.label3 = Label(self.grpSetpoint, text = 'DPG T (' +chr(176) + 'C):')
        self.label3.grid(row = 2, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb3 = Spinbox(self.grpSetpoint, from_ = 5, to_ = 50, width = 5)
        self.sb3.grid(row = 2, column = 1, padx = 2, pady = 2, sticky='w')
        self.label4 = Label(self.grpSetpoint, text = 'RH (%):')
        self.label4.grid(row = 3, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb4 = Spinbox(self.grpSetpoint, from_ = 1, to_ = 99, width = 5)
        self.sb4.grid(row = 3, column = 1, padx = 2, pady = 2, sticky='w')


