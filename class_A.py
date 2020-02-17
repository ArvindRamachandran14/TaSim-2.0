import global_var as gv

class A():

	def __init__(self):

		global a, b, c

		self.g = gv.globals()

		self.a = self.g.a

		self.b = self.g.b

		self.c = self.g.c


	def modify(self):

		print(self.g.a)

		print(self.g.c)

		self.g.a = 5

		self.g.c = [1,2]

		print(self.g.a)

		print(self.g.c)

obj_a = A()

obj_a.modify()




