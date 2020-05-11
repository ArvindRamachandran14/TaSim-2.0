# Echo client program
import socket

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
for i in range(3) :
	s.sendall(b'Hello, world')
	data = s.recv(1024)
	print('Received', repr(data))
s.sendall(b'exit')	
data = s.recv(1024)
print('Received', repr(data))
s.close()
print('Received', repr(data))