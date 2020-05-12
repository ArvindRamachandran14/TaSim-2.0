# CtrlConfig.py
# Class to define content of the config tab.
#
# Change history:
#   20191115:KDT - Original issue

from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton
import Data_coord
from math import exp
from sympy.solvers import solve
from sympy import Symbol
import scipy.optimize as opt

class CtrlSetup(Frame) :
    def __init__(self, parent, cons, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.cons = cons
        self.parent = parent
        self.buildContent()

    def buildContent(self) :
        self.output = StringVar()
        self.grpSetpoint = LabelFrame(self, text = ' Control Variables ')
        self.grpSetpoint.grid(row=0,column=0, padx=10, pady=10)
        self.label1 = Label(self.grpSetpoint, text = 'Sample Chamber T (' +chr(176) + 'C):')
        self.label1.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb1 = Spinbox(self.grpSetpoint, from_ = 5, to_ = 50, width = 5)
        self.sb1.grid(row = 0, column = 1, padx = 2, pady = 2, sticky='w')
        #self.sb1.bind("<Return>", self.send_command)
        self.label2 = Label(self.grpSetpoint, text = 'Conditioning Chamber T (' +chr(176) + 'C):')
        self.label2.grid(row = 1, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb2 = Spinbox(self.grpSetpoint, from_ = 5, to_ = 50, width = 5)
        self.sb2.grid(row = 1, column = 1, padx = 2, pady = 2, sticky='w')

        self.label3 = Label(self.grpSetpoint, text = 'RH (%):')
        self.label3.grid(row = 2, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb3 = Spinbox(self.grpSetpoint, from_ = 1, to_ = 100, width = 5)
        self.sb3.grid(row = 2, column = 1, padx = 2, pady = 2, sticky='w')
        self.label4 = Label(self.grpSetpoint, text="SC bypass:")
        self.label4.grid(row=3,column=0, padx = 2, pady = 2, sticky='e')

        MODES = [("ON", "1"),("OFF", "2")]

        self.v = StringVar()
        self.v.set("2") # initialize

        for i in range(2):
            self.rb = Radiobutton(self.grpSetpoint, text=MODES[i][0], variable=self.v, value=MODES[i][1])
            self.rb.grid(row=3, column=i+1, padx = 2, pady = 2, sticky='w')

        self.output_text = Label(self.grpSetpoint, borderwidth=1, width=5, textvariable=self.output)
        self.output_text.grid(row = 4, column = 0, columnspan=2, padx = 2, pady = 2)

        self.box_values = Button(self.grpSetpoint, text="Send box values", command=self.send_command)
        self.box_values.grid(row = 5, column = 1, columnspan=2, padx = 2, pady = 2, sticky='w')


    def send_command(self): 

        #print(self.sb1.get(), self.sb2.get(), self.sb3.get(), self.sb4.get())  
        
        reply1 = self.cons.send_command_to_PC('s TSC '+  self.sb1.get())

        reply2 = self.cons.send_command_to_PC('s TCC '+  self.sb2.get())

        target_pressure = (float(self.sb3.get())/100.0)*self.ph2oSat(float(self.sb1.get()))

        target_TDP = opt.brentq(lambda T: self.ph2oSat_solve(T, target_pressure), -50, 50)

        reply3 = self.cons.send_command_to_PC('s TDP '+  str(target_TDP))

        #if reply1 == reply2 == reply3 == 'OK':

        #self.output.set("Ok")

        #self.output.set("")

    def ph2oSat_solve(self, T, P):
        return 610.78 * exp((T * 17.2684) / (T + 238.3)) - P

    def ph2oSat(self, T):
        return 610.78 * exp((T * 17.2684) / (T + 238.3))


