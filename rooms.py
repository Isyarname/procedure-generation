from matrix_reload import *
from random import randint, choice, shuffle
import copy
import time


class Room(Matrix):
	def __init__(self, width=3, height=3, homogeneous=False, value=7, ls=[], coordinates=[0,0]):
		Matrix.__init__(self, width, height, homogeneous, value, ls, coordinates)
		self.value = value
		self.canExpand = True
		self.colDir = []
		self.numberOfOutputs = 0
		self.directions = ["left", "right", "up", "down"]

	def glue(self, m, allowList=["#", 0]):
		y, x = m.coordinates
		h, w = m.height, m.width
		for i, o in enumerate(m):
			for j, oo in enumerate(o):
				if self.body[i+y][j+x] in allowList:
					self.body[i+y][j+x] = oo

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


def main():
	width = 30
	height = 30
	matrix = Room(width, height, homogeneous=True, value=0)
	#testMatrix = Matrix(width, height, homogeneous=True, value=0)
	rooms = []
	depth = 5
	quantity = 4
	for i in range(quantity):
		r = Room(depth, depth, coordinates=[randint(depth,height-1-depth), randint(depth,width-1-depth)])
		rooms.append(r)
		while impositionChecker(i, rooms):
			print("imposition")
			rooms[i].coordinates = [randint(depth,height-1-depth), randint(depth,width-1-depth)]

		
	canExpand = True
	while canExpand:
		canExpand = False
		for i, r in enumerate(rooms):
			if rooms[i].canExpand:
				rooms[i].expand()
				roomChecker(rooms[i], i, rooms, matrix)
			if rooms[i].canExpand:
				canExpand = True
		matrix.matrixJoiner(rooms)
		print(matrix)
		time.sleep(0.1)
	corridors = corridorsCreator(rooms, matrix)
	#matrix.matrixJoiner(corridors, symbols="ccccccccccccccccccc")
	for i, o in enumerate(corridors):
		matrix.glue(o)
	print(matrix)
	print(corridors)

def corridorsCreator(rooms, matrix):		
	corridors = []
	symbols = "./^<—+|\\>L?-*:JZxbMc"
	allowList = ["#", 0]
	for i, r in enumerate(rooms):
		directions = ["left", "right", "up", "down"]
		shuffle(directions)
		y0, x0 = r.coordinates
		h, w = r.height, r.width
		for dir in directions:
			if dir == "left":
				exitFlag = False
				for y in range(y0+1, y0+h-1):
					for j, x in enumerate(range(x0-1, -1, -1)):
						if str(matrix[y][x]) in symbols:
							corridor = Room(j+1, 3, homogeneous=True, value="c", coordinates=[y-1, x+1])
							corridor.walls(axis="x")
							print(corridor.coordinates)
							print(corridor.height, corridor.width)
							matrix.glue(corridor, allowList)
							exitFlag = True
							break
						elif str(matrix[y][x]) == "c":
							exitFlag = True
							break
					if exitFlag:
						break

			elif dir == "right":
				exitFlag = False
				for y in range(y0+1, y0+h-1):
					for j, x in enumerate(range(x0+w, matrix.height)):
						if str(matrix[y][x]) in symbols:
							corridor = Room(j+1, 3, homogeneous=True, value="c", coordinates=[y-1, x0+w-1])
							corridor.walls(axis="x")
							print(corridor.coordinates)
							print(corridor.height, corridor.width)
							matrix.glue(corridor, allowList)
							exitFlag = True
							break
					if exitFlag:
						break

			elif dir == "up":
				exitFlag = False
				for x in range(x0+1, x0+w-1):
					for j, y in enumerate(range(y0-1, -1, -1)):
						if str(matrix[y][x]) in symbols:
							corridor = Room(3, j+1, homogeneous=True, value="c", coordinates=[y+1, x-1])
							corridor.walls(axis="y")
							matrix.glue(corridor, allowList)
							print(corridor.coordinates)
							print(corridor.height, corridor.width)
							exitFlag = True
							break
					if exitFlag:
						break

			elif dir == "down":
				exitFlag = False
				for x in range(x0+1, x0+w-1):
					for j, y in enumerate(range(y0+h, matrix.height)):
						if str(matrix[y][x]) in symbols:
							corridor = Room(3, j+1, homogeneous=True, value="c", coordinates=[y0+h-1, x-1])
							corridor.walls(axis="y")
							matrix.glue(corridor, allowList)
							print(corridor.coordinates)
							print(corridor.height, corridor.width)
							exitFlag = True
							break
					if exitFlag:
						break
			
	return corridors

def impositionChecker(i, rooms):
	y1, x1 = rooms[i].coordinates
	h1, w1 = rooms[i].height, rooms[i].width
	for rid, room in enumerate(rooms):
		y2, x2 = room.coordinates
		h2, w2 = room.height, room.width
		if rid != i:
			if (y2 <= y1 + h1 and
				y2 + h2 >= y1 and 
				x1 <= x2 + w2 and
				x1 + w1 >= x2):
				return True


def roomChecker(rm, i, rooms, matrix):
	y1, x1 = rm.coordinates
	h1, w1 = rm.height, rm.width

	if (y1 == 0 or x1 == 0 or
		y1 + h1 == matrix.height or
		x1 + w1 == matrix.width):
		rm.canExpand = False
		print("#1")
		return True

	for rid, room in enumerate(rooms):
		y2, x2 = room.coordinates
		h2, w2 = room.height, room.width
		if rid != i:
			if (y2 <= y1 + h1 - 1 and
				y2 + h2 - 1 >= y1):
				if (x1 + w1 == x2 or
					x1 == x2 + w2):
					rm.canExpand = False
					room.canExpand = False
					print("#2")
					return True

			if (x1 <= x2 + w2 - 1 and
				x1 + w1 - 1 >= x2):
				if (y1 + h1 == y2 or
					y1 == y2 + h2):
					rm.canExpand = False
					room.canExpand = False
					return True





'''r = Room()
print(r)
r.expand()
r.update()
print(r)'''

if __name__ == '__main__':
	main()