# CtrlConfig.py
# Class to define content of the config tab.
#
# Change history:
#   20191115:KDT - Original issue

from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar
import Data_coord

class CtrlSetup(Frame) :
    def __init__(self, parent, cons, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.cons = cons
        self.parent = parent
        self.buildContent()

    def buildContent(self) :
        self.output = StringVar()
        self.grpSetpoint = LabelFrame(self, text = ' Setpoints ')
        self.grpSetpoint.grid(row=0,column=0, padx=10, pady=10)
        self.label1 = Label(self.grpSetpoint, text = 'Sample Chamber T (' +chr(176) + 'C):')
        self.label1.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb1 = Spinbox(self.grpSetpoint, from_ = 5, to_ = 50, width = 5)
        self.sb1.grid(row = 0, column = 1, padx = 2, pady = 2, sticky='w')
        self.sb1.bind("<Return>", self.send_command)
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
        self.box_values = Button(self.grpSetpoint, text="Send box values", command=self.send_command)
        self.box_values.grid(row = 4, column = 0, columnspan=2, padx = 2, pady = 2)
        self.output_text = Label(self.grpSetpoint, borderwidth=1, width=5, textvariable=self.output)
        self.output_text.grid(row = 5, column = 0, columnspan=2, padx = 2, pady = 2)

    def send_command(self): 

        #print(self.sb1.get(), self.sb2.get(), self.sb3.get(), self.sb4.get())   
        
        reply1 = self.cons.send_command_to_PC('s TSC '+  self.sb1.get())

        reply2 = self.cons.send_command_to_PC('s TCC '+  self.sb2.get())

        reply3 = self.cons.send_command_to_PC('s TDP '+  self.sb2.get())

        #reply4 = self.cons.send_command_to_PC('s R '+  str(self.sb2.get()))s

        #if reply1 == reply2 == reply3 == 'OK':

        #self.output.set("Ok")

        #self.output.set("")


