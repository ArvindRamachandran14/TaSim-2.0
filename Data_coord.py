import serial

class Data_coord():

	def __init__(self):

		pass

	def Connect(self, serial_port, baud_rate, TAD_rec_count):

		self.ser_PC = serial.Serial(serial_port, baud_rate, timeout=3)

		return True

	def Disconnect(self):

		print('Disconnect')

		self.ser_PC.close()

		return False
