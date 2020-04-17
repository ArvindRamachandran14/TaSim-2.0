#! /usr/local/bin/python3 

from ctypes import c_int, c_double, c_byte, c_bool, Structure, sizeof
from random import random
import mmap
import os
from datetime import datetime
import asyncio
import platform
import socket

encoding = 'utf-8'
recCount = 21

class TAData(Structure) :
	_pack_ = 4
	_fields_ = [ \
		('recNum', c_int),
		('recTime', c_double),
		('status', c_int),
		('TCC', c_double),
		('TSC', c_double),
		('TDP', c_double),
		('Wgt', c_double),
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

class producer() :
	def __init__(self, interval) :
		self.startTime = None
		self.bDone = False
		self.interval = interval
		self.bForked = False
		self.recNum = 0
		self.taShare = None
		self.taData = None
		self.mmShare = None
		self.mmfd = None
		self.startTime = None
		self.sem = None				# Added semaphore instance here
		self.sock = None
		self.host = '127.0.0.1'		# localhost
		self.port = 50007
		self.initialize()

	# @asyncio.coroutine
	async def produce(self) :
		TCC = TSC = TDP = Wgt = pH2O = pCO2 = 0.0
		status = 0
		tash = TAShare.from_buffer(self.mmShare)
		while not self.bDone :
			async with self.sem :		# async with added here
				recIdx = tash.recIdx + 1
				if recIdx >= tash.recCount :
					recIdx = 0

				# Get some data
				taData = self.getDataFromTA('g all')

				# Get the time
				now = datetime.now()
				seconds = now.hour * 3600 + now.minute * 60 + now.second + now.microsecond / 1000000
				if self.startTime == None :
					self.startTime = seconds
				seconds = seconds - self.startTime
				tash.data[recIdx].recNum = self.recNum
				self.recNum += 1
				tash.data[recIdx].recTime = seconds

				if type(taData).__name__ == 'list' :
					(TCC, TSC, TDP, Wgt, pH2O, pCO2, status) = taData
					tash.data[recIdx].TCC = TCC
					tash.data[recIdx].TSC = TSC
					tash.data[recIdx].TDP = TDP
					tash.data[recIdx].Wgt = Wgt
					tash.data[recIdx].pH2O = pH2O
					tash.data[recIdx].pCO2 = pCO2
					tash.data[recIdx].status = status
				else :
					tash.data[recIdx].TCC = 0
					tash.data[recIdx].TSC = 0
					tash.data[recIdx].TDP = 0
					tash.data[recIdx].Wgt = 0
					tash.data[recIdx].pH2O = 0
					tash.data[recIdx].pCO2 = 0
					tash.data[recIdx].status = -1

				tash.recIdx = recIdx
				print('P: {0:4d} {1:10.3f} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f} {6:10.3f} {7:10.3} {8:d}'.format( \
					tash.data[recIdx].recNum, tash.data[recIdx].recTime, \
					tash.data[recIdx].TCC, tash.data[recIdx].TSC, tash.data[recIdx].TDP, \
					tash.data[recIdx].Wgt, tash.data[recIdx].pH2O, tash.data[recIdx].pCO2, \
					tash.data[recIdx].status))
				# semaphore is released here
			await asyncio.sleep(self.interval)
		return 0

	async def doCmd(self) :
		while not self.bDone :
			async with self.sem:			# async with added here to control access
				tash = TAShare.from_buffer(self.mmShare)
				command = bytearray(tash.command).decode(encoding).rstrip('\x00')
				if not command == '' :
					print(f'Command: {command}')
					for idx in range(0,80) :
						tash.reply[idx] = 0
						tash.command[idx] = 0
					if command == '@{EXIT}' :
						self.bDone = True
						sReply = 'OK'
					else :
						sReply = self.getDataFromTA(command)

					# Put the reply into the shared reply buffer
					repBuf = bytearray(sReply, encoding)
					tash.reply[0:len(repBuf)] = repBuf
					# Semaphore is released here
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
		self.sem = asyncio.Semaphore(1)			# Added semaphore creation
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.host, self.port))
	
	def getDataFromTA(self, cmd) :
		cmdBytes = bytearray(cmd, 'utf-8')
		try :
			self.sock.send(cmdBytes)
			rData = self.sock.recv(128)
		except Exception :
			retVal = -1
		else :
			sData = rData.decode('utf-8')
			if cmd == 'g all' :
				if sData[0] == 'v' :
					sData = sData[2:]
					vals = sData.split(',', 6)
					retval = [float(val) for val in vals]
					retval.append(0)			# for status
				else :
					retval = sData
			else :
				retval = sData
		return retval
		# if command == "g all" :
		# 	temp1 = 25 + 2 * (random() - 0.5)
		# 	temp2 = 15 + 2 * (random() - 0.5)
		# 	temp3 = 40 + 2 * (random() - 0.5)
		# 	pH2O = 3000 + 10 * (random() - 0.5)
		# 	pCO2 = 40 + 0.5 * (random() - 0.5)
		# 	status = 0
		# 	retval = (temp1, temp2, temp3, pCO2, pH2O, status)
		# else:
		# 	retval = '<' + command + '>'
		# return retval

# main program
async def main() :
	prod = producer(2)		# Interval argument
	task1 = asyncio.create_task(prod.produce())
	task2 = asyncio.create_task(prod.doCmd())
	await task1
	await task2
	print('Done')

asyncio.run(main())


