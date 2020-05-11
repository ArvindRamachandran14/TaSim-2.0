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
import Config
import TaModel
import pykbhit as pykb

# TaSim
# TODO: Revise class to handle TaModel
class TaSim() :
	def __init__(self, cfg) :
		self.cfg = cfg
		self.tam = TaModel.TaModel(cfg)
		self.kb = pykb.KBHit()
		self.cmdLine = ''
		self.deltaT = cfg.deltaT 
		self.bDone = False					# Done flag
		self.sel = None						# Selector
		self.host = ''						# Any host
		self.port = 50007					# ... on this port
		self.sock = None					# s is the socket
		self.conn = None					# conn is the connection
		self.addr = None					# addr is the address
		self.initSock()
		self.noList = ['no', 'off']
		self.bSockRecover = False			# Set when a socket recovery is needed

	# taCompute
	# Update the values at the specified interval.
	# @asyncio.coroutine
	def taCompute(self) :
		self.tam.cycle()

	# doReqCmd
	# This function does the command process for commands received via the socket.
	#   It handles the following commands:
	#	g <parm>, where parm in ['tcc', 'tsc', 'tdp', 'wgt', 'pco2', 'ph20', 'all']
	#	s <parm>, where parm in ['tcc', 'tsc', 'tdp']
	#	quit

	def doReqCmd(self, conn, mask) :
		bOK = False
		try :
			cmdBytes = conn.recv(128)
		except Exception :
			return bOK
		else :
			bOK = (len(cmdBytes) > 0)
		if bOK :		
			cmd = cmdBytes.decode('utf-8')
		else :
			return bOK
		reply = self.executeCmd(cmd)
		replyBytes = bytearray(reply, 'utf-8')
		try :
			conn.send(replyBytes)	 # send the reply
		except Exception :
			return bOK

	# doLocalCmd
	# Handles commands input locally.  It is called when a key is pressed on the 
	# keyboard.
	def doLocalCmd(self) :
		ch = self.kb.getch()
		if ord(ch) == 10 :
			reply = self.executeCmd(self.cmdLine)
			print(reply)
			self.cmdLine = ''
		else :
			self.cmdLine = self.cmdLine + ch

	# executeCmd
	# Execute the command passed in the argument.  It nandle set commands, get commands, and
	# quit.
	def executeCmd(self, cmd) :
		bOK = True
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
					dR = self.tam.data[self.tam.idx]
					if parm == 'tcc' :
						reply = 'v {0:.2f}'.format(dR.Tcc)
					elif parm == 'tsc' :
						reply = 'v {0:.2f}'.format(dR.Tsc)
					elif parm == 'tdp' :
						reply = 'v {0:.2f}'.format(dR.Tdp)
					elif parm == 'wgt' :
						reply = 'v {0:.2f}'.format(dR.Wgt)
					elif parm == 'ph2o' :
						reply = 'v {0:d}'.format(dR.ph2oSC)
					elif parm == 'pco2' :
						reply = 'v {0:d}'.format(dR.pco2SC)
					elif parm == 'all' :
						reply =  'v {0:.2f},{1:.2f},{2:.2f},{3:.2f},{4:.2f},{5:2f}'.format( \
							dR.Tcc, dR.Tsc, dR.Tdp, dR.Wgt, dR.ph2oSC, dR.pco2SC)
					else :
						reply = 'e INVPARM'
				elif cmdParts[0] == 's' :
					if len(cmdParts) >= 3 :
						reply = 'OK'
						sVal = cmdParts[2].lower()
						if parm == "bypass" :
							val = False if sVal in self.noList else True
							self.tam.sc.bBypass = val
						elif parm == "inject" :
							if len(cmdParts == 4) :
								try :
									volInj = float(cmdParts[2])
									pco2Inj = float(cmdParts[3])
									self.tam.cc.pco2Inj = pco2Inj
									self.tam.cc.volInj = volInj
								except :
									reply = 'e INVVAL'
								else :
									pass
							else :
								reply = 'e INVVAL'
						else :
							try :
								val = float(cmdParts[2])
							except Exception :
								reply = 'e INVVAL'
							else :
								if parm == 'tcc' :
									self.tam.cc.TCCset = val
								elif parm == 'tsc' :
									self.tam.sc.TSCset = val
								elif parm == 'tdp' :
									self.tam.dpg.TDPset = val
								else :
									reply = 'e INVPARM'
					else :
						reply = 'e INVPARM'
				else :
					reply = 'e INVCMD'

		return reply

	# accept methogd
	# Accept the connection
	def accept(self, sock, mask):
		self.conn, self.addr = self.sock.accept()  # Should be ready
		print('accepted', self.conn, 'from', self.addr)
		self.conn.setblocking(False)
		self.sel.register(self.conn, selectors.EVENT_READ, self.doReqCmd)
		self.bSockRecover = False
		return True

	# taAccept
	# Use the selector to 
	def taAccept(self) :
		tTimeout = 0.1						# select timeout time
		nCompute = int(self.deltaT / tTimeout)
		n = nCompute - 1
		while not self.bDone :
			events = self.sel.select(tTimeout)
			for key, mask in events:
				bOK = True
				callback = key.data
				bOK = callback(key.fileobj, mask)
				if not bOK and not self.bSockRecover :
					self.conn.close()
					self.sel.unregister(self.conn)
					self.sel.unregister(self.sock)
					self.sel.register(self.sock, selectors.EVENT_READ, self.accept)	
					self.bSockRecover = True
			if self.kb.kbhit() :
				self.doLocalCmd()
			n += 1
			if (n % nCompute) == 0 :
				self.taCompute()		
		
	def initSock(self) :
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
	print("TaSim V0.90.00")
	cfg = Config.Config()
	cfg.ReadConfig('tasim.ini')
	taSim = TaSim(cfg)
	taSim.taAccept()
	print('Done')

# Main program
main()


