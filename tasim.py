# tasim.py
# Thermo-Analyzer simulator.
# 20200322 - Original.
#
#
# This module implements the TaSim class, which simulates the operation of the
# Thermo-Analyzer (TA).  The class implements three temperature controls, three
# temperature sensors, one weight sensor, one pCO2 sensor, and one pH2O sensor.
#
# The temperature sensors are coupled to the temperature sensors via a differential
# solution that implements a simple exponential change curve.  Each of the volumne:
# Conditioning Chamber, Sample Chamber, and Dew Point reservoir have differnt time
# constants.
#
# For now, the weight, pCO2, and pH2O sensors return constants.  The idea is that
# this simulation can be expanded to implement coupling between TDP and TSC
# (DewPoint and Sample Chamber temperatures), and the pCO2 and pH2O values can be
# modeled by some kind of sorbent.  (KT: I have not thought about all of this yet.)
#
# So that this can be run on a single PC, this module implements a listening socket
# that accepts a connection from a TADAQ instance.  The TADAQ, actually the producer
# in the shm module, will be changed to connect with the socket opened by the TaSim.

import os
from datetime import datetime
# import asyncio
import platform
import selectors
import socket
from math import exp

class TaSim() :
	def __init__(self, tauCC, tauSC, tauDP) :
		self.tauTCC = tauCC				# Time constants
		self.tauTSC = tauSC
		self.tauTDP = tauDP
		self.TCCset = 20					# Set point parameters
		self.TSCset = 20
		self.TDPset = 20
		self.TCC = 20						# Initialized parameters
		self.TSC = 20
		self.TDP = 20
		self.Wgt = 2						# grams
		self.pH2O = 20000					# Pa 
		self.pCO2 = 40						# platform
		self.TCC_1 = 20						# Needed for computation
		self.TSC_1 = 20
		self.TDP_1 = 20
		self.TCCfactor = 0
		self.TSCfactor = 0
		self.TDPfactor = 0
		self.deltaT = 0.2					# 200 ms iteration rate
		self.bDone = False					# Done flag
		self.sel = None						# Selector
		self.host = ''						# Any host
		self.port = 50007					# ... on this port
		self.sock = None					# s is the socket
		self.conn = None					# conn is the connection
		self.addr = None					# addr is the address
		self.count = 0
		self.initialize()

	# taCompute
	# Update the values at the specified interval.
	# @asyncio.coroutine
	def taCompute(self) :
		# Update the temperatures
		self.TCC_1 = self.TCC
		self.TCC = self.TCCset + (self.TCC_1 - self.TCCset) * self.TCCfactor
		self.TSC_1 = self.TSC
		self.TSC = self.TSCset + (self.TSC_1 - self.TSCset) * self.TSCfactor
		self.TDP_1 = self.TDP
		self.TDP = self.TDPset + (self.TDP_1 - self.TDPset) * self.TDPfactor

		# For now, the weight, pCO2, and pH2O are constant
		# ... so nothing to do.  More can be added here when or if we 
		# ever need or want to do it.
		# await asyncio.sleep(self.deltaT)

	# doReqCmd
	# This function does the command process.  It handles the following commands:
	#	g <parm>, where parm in ['tcc', 'tsc', 'tdp', 'wgt', 'pco2', 'ph20', 'all']
	#	s <parm>, where parm in ['tcc', 'tsc', 'tdp']
	#	quit

	def doReqCmd(self, conn, mask) :
		bOK = True
		try :
			cmdBytes = conn.recv(128)
		except Exception :
			return
		cmd = cmdBytes.decode('utf-8')
		# print(cmd)
		if cmd == 'quit' :
			self.bDone = True
			reply = cmd
		else :
			# Handle the command
			cmd = cmd.lower()
			cmdParts = cmd.split(' ', 3)
			if len(cmdParts) < 2 :
				reply = 'e INVCMD'
				bOK = False

			if bOK :
				parm = cmdParts[1]

			if bOK :
				if cmdParts[0] == 'g' :
					if parm == 'tcc' :
						reply = 'v {0:.2f}'.format(self.TCC)
					elif parm == 'tcc' :
						reply = 'v {0:.2f}'.format(self.TSC)
					elif parm == 'tsc' :
						reply = 'v {0:.2f}'.format(self.TSC)
					elif parm == 'tdp' :
						reply = 'v {0:.2f}'.format(self.TDP)
					elif parm == 'wgt' :
						reply = 'v {0:.2f}'.format(self.Wgt)
					elif parm == 'ph2o' :
						reply = 'v {0:d}'.format(self.pH2O)
					elif parm == 'pco2' :
						reply = 'v {0:d}'.format(self.pCO2)
					elif parm == 'all' :
						reply =  'v {0:.2f},{1:.2f},{2:.2f},{3:.2f},{4:d},{5:d}'.format( \
							self.TCC, self.TSC, self.TDP, self.Wgt, self.pH2O, self.pCO2)
					else :
						reply = 'e INVPARM'
				elif cmdParts[0] == 's' :
					if len(cmdParts) == 3 :
						try :
							val = float(cmdParts[2])
						except Exception :
							reply = 'e INVVAL'
						else :
							reply = 'OK' 
							if parm == 'tcc' :
								self.TCCset = val
							elif parm == 'tsc' :
								self.TSCset = val
							elif parm == 'tdp' :
								self.TDPset = val
							else :
								reply = 'e INVPARM'
					else :
						reply = 'e INVPARM'
				else :
					reply = 'e INVCMD'

		replyBytes = bytearray(reply, 'utf-8')
		try :
			conn.send(replyBytes)	 # send the reply
		except Exception :
			return

	# accept methogd
	# Accept the connection
	def accept(self, sock, mask):
		self.conn, self.addr = self.sock.accept()  # Should be ready
		print('accepted', self.conn, 'from', self.addr)
		self.conn.setblocking(False)
		self.sel.register(self.conn, selectors.EVENT_READ, self.doReqCmd)

	# taAccept
	# Use the selector to 
	def taAccept(self) :
		while not self.bDone :
			events = self.sel.select(self.deltaT)
			for key, mask in events:
				callback = key.data
				callback(key.fileobj, mask)	
			self.taCompute()		
		
	def initialize(self) :
		self.TCCfactor = exp(-self.deltaT/self.tauTCC)
		self.TSCfactor = exp(-self.deltaT/self.tauTSC)
		self.TDPfactor = exp(-self.deltaT/self.tauTDP)
		self.sel = selectors.DefaultSelector()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))
		self.sock.listen(100)
		self.sock.setblocking(0)
		self.sel.register(self.sock, selectors.EVENT_READ, self.accept)

# main program
# Modify the taSim line to change the time constants
def main() :
	taSim = TaSim(30, 20, 10)
	taSim.taAccept()
	print('Done')

# Main program
main()


