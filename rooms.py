from matrix_reload import *
from random import randint


class Room(Matrix):
	def __init__(self, width=3, height=3, homogeneous=False, value=7, ls=[], coordinates=[0,0]):
		Matrix.__init__(self, width, height, homogeneous, value, ls, coordinates)
		self.value = value
		self.canExpand = True
		self.colDir = []
		self.numberOfOutputs = 0
		self.directions = ["left", "right", "up", "down"]
		self.neighbours = []

	def glue(self, m, allowList=["#", 0]):
		y, x = m.coordinates
		h, w = m.height, m.width
		for i, o in enumerate(m):
			for j, oo in enumerate(o):
				try:
					if self.body[i+y][j+x] in allowList:
						self.body[i+y][j+x] = oo
				except IndexError as ie:
					print("y, x:", y, x)
					print("index:", i+y, j+x)
					print(ie)

	def walls(self, axis, value="#"):
		w = self.width
		h = self.height
		if axis == "x":
			self.rectangle(0, 0, w, 1, value)
			self.rectangle(0, h-1, w, 1, value)
		elif axis == "y":
			self.rectangle(0, 0, 1, h, value)
			self.rectangle(w-1, 0, 1, h, value)

	def bordürtschiki(self, value=0):
		w = self.width
		h = self.height
		self.rectangle(0, 0, w, 1, value)
		self.rectangle(0, h-1, w, 1, value)
		self.rectangle(0, 1, 1, h, value)
		self.rectangle(w-1, 1, 1, h, value)

	def expand(self):
		"""
		0 - left
		1 - up
		2 - right
		3 - down
		"""
		dir = randint(0, 3)
		if dir == 0:
			if self.coordinates[1] > 0:
				self.coordinates[1] -= 1
				self.width += 1
			else:
				print("baaaaaaaaaaaaa")
		elif dir == 1:
			self.coordinates[0] -= 1
			self.height += 1
		elif dir == 2:
			self.width += 1
		elif dir == 3:
			self.height += 1
		self.update()

	def update(self):
		self.body = []
		for i in range(self.height):
			temp = []
			for j in range(self.width):
				temp.append(self.value)
			self.body.append(temp)
