#! /usr/local/bin/python3 
# -*- coding: utf-8 -*-

# This is a conumer example.

import serial
from ctypes import c_int, c_double, c_byte, c_bool, Structure, sizeof
from random import random
import mmap
import os
from datetime import datetime
import asyncio
from subprocess import Popen
#import pykbhit as pykb


encoding = 'utf-8'
loop = None
recCount = 21

class TAData(Structure) :
	_pack_ = 4
	_fields_ = [ \
		('recNum', c_int),
		('recTime', c_double),
		('status', c_int),
		('temp1', c_double),
		('temp2', c_double),
		('temp3', c_double),
		('pH2O', c_double),
		('pCO2', c_double)]

class TAShare(Structure) :
	_pack_ = 4
	_fields_ = [ \
			('command', c_byte * 80),
			('reply', c_byte * 80),
			('recCount', c_int),
			('recIdx', c_int),
			('data', TAData * recCount)]

class consumer() :
	def __init__(self, interval) :
		self.startTime = None
		self.bDone = False
		self.interval = interval
		self.recNum = 0
		self.taShare = None
		self.taData = None
		self.mmShare = None
		self.mmfd = None
		self.lastIdx = -1
		self.recsGot = 0
		self.initialize()
		self.kb = pykb.KBHit()

	# consume
	# This function gets unread data from the shared memory circular
	# buffer at the specified interval.
	async def consume(self) :
		while not self.bDone :
			tash = TAShare.from_buffer(self.mmShare)
			while not self.lastIdx == tash.recIdx :
				self.lastIdx += 1
				if self.lastIdx == recCount :
					self.lastIdx = 0
				tad = TAData.from_buffer(tash.data[self.lastIdx])

				# The only thing done with the data is to print it here.
				print('P: {0:4d} {1:10.3f} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f} {6:10.3f} {7:10.3f} {8:10.3f} {9:10.3f} {10:d}'.format( \
                    tad.recNum, tad.recTime, \
                    tad.SC_T1, tad.SC_T2, tad.CC_T1, tad.DPG_T1, \
                    tad.pH2O, tad.pCO2, tad.Dew_point_temp, \
                    tad.Sample_weight, tad.Status))

				self.recsGot += 1

			await asyncio.sleep(self.interval)
		return 0

	def initialize(self) :
		self.mmfd = open('taShare', 'r+b')

async def main() :

	cons = consumer(2)

	print('Type \"Exit\" when ready to quit...')
	task1 = asyncio.create_task(cons.consume())
	#task2 = asyncio.create_task(cons.getCmd())
	await task1
	#await task2


class Data_coord():

	def __init__(self):

		pass

	def Connect(self, serial_port, baud_rate, time_out):

		Popen(['python3.7', 'TADAQ.py', serial_port, baud_rate, time_out])

	def Disconnect(self):

		cmdBuf = bytearray('@{EXIT}', encoding)

		tash.command[0:len(cmdBuf)] = cmdBuf

		print('Disconnect')

		g.bconnected = "False"

		g.update()

		#self.ser_PC.close()

	#def submit():
