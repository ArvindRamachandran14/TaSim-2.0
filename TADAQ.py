#! /usr/local/bin/python3 
# -*- coding: utf-8 -*-

from ctypes import c_int, c_double, c_byte, c_bool, Structure, sizeof #creates c type structures
from random import random #random numbers
import mmap #memory map
import os 
from datetime import datetime

import datetime as dt 

import asyncio #timing to work right asychronous call - go and read the data and the meanwhile you can do other things
import serial
import xml.etree.ElementTree as ET
import time

import global_tech_var as g

import sys
import json

encoding = 'utf-8' # covers straight ascii 8 bit char codes 
loop = None #variable timeer uses
recCount = 21 #how many records are in the shared memory 


class TAData(Structure) :
    _pack_ = 4
    _fields_ = [ \
        ('recNum', c_int),
        ('recTime', c_double),
        ('SC_T1', c_double),
        ('SC_T2', c_double),
        ('CC_T1', c_double),
        ('DPG_T1', c_double),
        ('pH2O', c_double),
        ('pCO2', c_double),
        ('Dew_point_temp', c_double),
        ('Sample_weight', c_double),
        ('Status', c_int)
        ]

class TAShare(Structure) :
    _pack_ = 4
    _fields_ = [ \
            ('command', c_byte * 80), # 80 byte buffer
            ('reply', c_byte * 80),
            ('recCount', c_int),
            ('recIdx', c_int),
            ('data', TAData * recCount)]

class producer() :

    def __init__(self, ser) :
        self.ser = ser
        self.startTime = None
        self.bDone = False
        #self.bForked = False
        self.recNum = 0
        self.taShare = None
        self.taData = None
        self.mmShare = None
        self.mmfd = None
        self.startTime = None
        self.flag = False

        self.initialize()
       

    async def produce(self) :
            temp1 = temp2 = temp3 = pH2O = pCO2 = 0.0
            status = 0
            tash = TAShare.from_buffer(self.mmShare)
            while not self.bDone :
                recIdx = tash.recIdx + 1
                if recIdx >= tash.recCount :
                    recIdx = 0

                # Get some data

                data_list = self.getDataFromTA(self.ser)

                # Get the time
                now = datetime.now()
                seconds = now.hour * 3600 + now.minute * 60 + now.second + now.microsecond / 1000000
                if self.startTime == None :
                    self.startTime = seconds
                seconds = seconds - self.startTime

                tash.data[recIdx].recNum = self.recNum
                self.recNum += 1
                tash.data[recIdx].recTime = seconds
                tash.data[recIdx].SC_T1 = data_list[0]
                tash.data[recIdx].SC_T2 = data_list[1]
                tash.data[recIdx].CC_T1 = data_list[2]
                tash.data[recIdx].DPG_T1 = data_list[3]
                tash.data[recIdx].pH2O = data_list[4]
                tash.data[recIdx].pCO2 = data_list[5]
                tash.data[recIdx].Dew_point_temp = data_list[6]
                tash.data[recIdx].Sample_weight = data_list[7]
                tash.data[recIdx].Status = data_list[8]
                tash.recIdx = recIdx
                '''
                print('P: {0:4d} {1:10.3f} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f} {6:10.3f} {7:10.3f} {8:10.3f} {9:10.3f} {10:d}'.format( \
                        tash.data[recIdx].recNum, tash.data[recIdx].recTime, \
                        tash.data[recIdx].SC_T1, tash.data[recIdx].SC_T2, tash.data[recIdx].CC_T1, tash.data[recIdx].DPG_T1, \
                        tash.data[recIdx].pH2O, tash.data[recIdx].pCO2, tash.data[recIdx].Dew_point_temp, \
                        tash.data[recIdx].Sample_weight, tash.data[recIdx].Status))
                '''
                await asyncio.sleep(float(g.time_interval))

            return 0
    
    async def doCmd(self) :
        while not self.bDone :
            tash = TAShare.from_buffer(self.mmShare)
            command = bytearray(tash.command).decode(encoding).rstrip('\x00')
            if not command == '' :
                for idx in range(0,80) :
                    tash.reply[idx] = 0
                    tash.command[idx] = 0
                if command == '@{EXIT}' :
                    self.bDone = True
                    sReply = 'OK'

                elif command == '@{PAUSEDATAON}':
                    self.flag = True
                    sReply = 'OK'

                elif command == '@{PAUSEDATAOFF}':
                    self.flag = True
                    sReply = 'OK'

                elif command[0] == 'g' or 's':

                        self.ser.write(command.encode())

                        sReply = self.ser.readline().decode()
                    
                print(f'Command: {command}')
                #sReply = 'OK'
                repBuf = bytearray(sReply, encoding)
                tash.reply[0:len(repBuf)] = repBuf
            await asyncio.sleep(0.050)
        self.mmfd.close()

    def initialize(self) :
        tempTASH = TAShare()
        tempTASH.command[0:80] = [0] * 80
        tempTASH.reply[0:80] = [0] * 80
        tempTASH.recCount = recCount
        tempTASH.recIdx = -1
        self.mmfd = open('taShare', 'w+b')
        L = self.mmfd.write(tempTASH)
        self.mmfd.flush()
        print('Mapped size: ', L)
        self.mmShare = mmap.mmap(self.mmfd.fileno(), sizeof(tempTASH))   

    def getDataFromTA(self, ser) :

        #print(dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

        if not self.flag: 

            ser.write('g-all\n'.encode())

            Output_string = ser.readline().decode()

        #print(dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

        Split_strings_list  = Output_string.split(',')

        data_list = []

        for i in range(9):
            
            if i < 8:

                data_list.append(float(Split_strings_list[i]))

            else:
                
                data_list.append(int(Split_strings_list[i]))

        return(data_list)

# main program
async def main() :

    with open(g.cfgFile, 'r') as fCfg :
        config = json.loads(fCfg.read())        # Read config file
        g.initialize(config)              # Initialize the globals

    port = sys.argv[1]
    baud_rate = sys.argv[2]
    time_out = int(sys.argv[3])
    ser = serial.Serial(port, baud_rate, timeout=time_out)

    ser.write('c-check\n'.encode())

    reply = ser.readline().decode()

    #print('TADAQ reply was', reply)

    if reply == "Ok\r\n":

        #print('TADAQ reply was', reply)
   
        g.bconnected = "True"

        g.update()

    time.sleep(1)

    ser.reset_input_buffer()

    ser.reset_output_buffer()

    if g.bconnected == "True":

        ser.write('\n'.encode())

        prod = producer(ser)      # Number of records and interval
        task1 = asyncio.create_task(prod.produce())
        task2 = asyncio.create_task(prod.doCmd())
        await task1
        await task2
        print('Done')

asyncio.run(main())
