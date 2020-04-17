# socktest.py

import socket
import sys
import os

class sockTerm() :
	def __init__(self) :
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = '127.0.0.1'		# localhost
		self.port = 50007
		self.bDone = False
		self.sock.connect((self.host, self.port))

	def terminal(self) :
		while not self.bDone :
			print("socktest> ", end='')			# prompt
			cmd = sys.stdin.readline()
			cmd = cmd[:-1]
			print(cmd)
			if cmd == 'quit' :
				self.bDone = True
			cmdBytes = bytearray(cmd, 'utf-8')
			self.sock.send(cmdBytes, len(cmdBytes))
			replyBytes = self.sock.recv(128)
			reply = replyBytes.decode('utf-8')
			sys.stdout.write(reply + '\n')
			self.sock.close()

def main() :
	st = sockTerm()
	st.terminal()

main()



