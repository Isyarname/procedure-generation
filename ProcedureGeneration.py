from rooms import Room
from matrix_reload import Matrix
from random import randint, choice, shuffle
import copy


class GenAlgorithm:
	def __init__(self):
		pass

	def filter(self, matrix, width, height):
		for i in range(height):
			for j in range(width):
				if matrix[i][j] == "#":
					matrix[i][j] = 2
				elif str(matrix[i][j]) in "./^<—+|\\>L?-*:JZxbMc":
					matrix[i][j] = 1
				
		return matrix


class BSPTree(GenAlgorithm):
	def __init__(self):
		pass

	def splitMatrix(self, matrix, value=0, border=4):
		ms = []
		y, x = matrix.coordinates
		h, w = matrix.height, matrix.width
		if h == w:
			if randint(0,1) == 1:
				tx = randint(border, w-border)
				ms.append(Matrix(width=tx, height=h, homogeneous=True, value=value, coordinates=[y, x]))
				ms.append(Matrix(width=h-tx, height=h, homogeneous=True, value=value+1, coordinates=[y, x+tx]))
			else:
				ty = randint(border, h-border)
				ms.append(Matrix(width=w, height=ty, homogeneous=True, value=value, coordinates=[y, x]))
				ms.append(Matrix(width=w, height=h-ty, homogeneous=True, value=value+1, coordinates=[y+ty, x]))
		elif h > w:
			ty = randint(border, h-border)
			ms.append(Matrix(width=w, height=ty, homogeneous=True, value=value, coordinates=[y, x]))
			ms.append(Matrix(width=w, height=h-ty, homogeneous=True, value=value+1, coordinates=[y+ty, x]))
		else:
			tx = randint(border, w-border)
			ms.append(Matrix(width=tx, height=h, homogeneous=True, value=value, coordinates=[y, x]))
			ms.append(Matrix(width=w-tx, height=h, homogeneous=True, value=value+1, coordinates=[y, x+tx]))

		return ms

	def split(self, matrix, border=4):
		ms = self.splitMatrix(matrix, 0, border)
		btb = matrix.width >= border*2 and matrix.height >= border*2
		count = 0
		if not btb:
			print("МАЛЕНЬКАЯ МАТРИЦА!!!!!!!!!!!")
		while btb:
			temp = []
			btb = False
			for i, o in enumerate(ms):
				if o.width >= border*2 and o.height >= border*2:
					btb = True
					ms.pop(i)
					ms.extend(self.splitMatrix(o, count, border))
			count += i

		return ms

	def matrixJoiner(self, ml, matrix):
		symbols = "./^<—+|\\>L?-*:JZxbM"
		for i, o in enumerate(ml):
			o.fill(symbols[i:i+1])
			o.bordürtschiki(value="#")
			matrix.glue(o)

	def generate(self, height=30, width=30):
		matrix = Matrix(width, height, homogeneous=True, value=0)
		ms = self.split(matrix)
		self.matrixJoiner(ms, matrix)
		matrix.bordürtschiki(value="#")
		return self.filter(matrix, width, height)



class Planning(GenAlgorithm):
	def __init__(self):
		pass

	def generate(self, width=30, height=30, numberOfRooms=4, depth=5):
		matrix = Room(width, height, homogeneous=True, value=0)
		#testMatrix = Matrix(width, height, homogeneous=True, value=0)
		rooms = []
		for i in range(numberOfRooms):
			r = Room(depth, depth, coordinates=[randint(depth,height-1-depth), randint(depth,width-1-depth)])
			rooms.append(r)
			while self.impositionChecker(i, rooms):
				print("imposition")
				rooms[i].coordinates = [randint(depth,height-1-depth), randint(depth,width-1-depth)]

			
		canExpand = True
		while canExpand:
			canExpand = False
			for i, r in enumerate(rooms):
				if rooms[i].canExpand:
					rooms[i].expand()
					self.roomChecker(rooms[i], i, rooms, matrix)
				if rooms[i].canExpand:
					canExpand = True
			matrix.matrixJoiner(rooms)
			print(matrix)
		corridors = self.corridorsCreator(rooms, matrix)
		for i, o in enumerate(corridors):
			matrix.glue(o)
		return self.filter(matrix, width, height)

	def corridorsCreator(self, rooms, matrix):		
		corridors = []
		symbols = "./^<—+|\\>L?-*:JZxbMc"
		allowList = ["#", 0]
		for i, r in enumerate(rooms):
			directions = ["left", "right", "up", "down"]
			shuffle(directions)
			y0, x0 = r.coordinates
			h, w = r.height, r.width
			for dir in r.directions:
				if dir == "left":
					exitFlag = False
					for y in range(y0+1, y0+h-1):
						for j, x in enumerate(range(x0-1, -1, -1)):
							if x == 0:
								print("x000000000000!!!!!!!!!")
							if str(matrix[y][x]) in symbols or x == 0:
								
								corridor = Room(j+1, 3, homogeneous=True, value="c", coordinates=[y-1, x+1])
								corridor.walls(axis="x")
								matrix.glue(corridor, allowList)
								print(matrix)
								if x != 0:
									print(y, x)
									r2id = self.collisionChecker((y,x), rooms)
									rooms[r2id].directions.remove("right")
								r.directions.remove("left")
								exitFlag = True
								break
						if exitFlag:
							break

				elif dir == "right":
					exitFlag = False
					for y in range(y0+1, y0+h-1):
						for j, x in enumerate(range(x0+w, matrix.width)):
							if x == matrix.width:
								print("x==matrix.width!!!!!!!!!!!!")
							if str(matrix[y][x]) in symbols or x == matrix.width-1:
								
								corridor = Room(j+1, 3, homogeneous=True, value="c", coordinates=[y-1, x0+w-1])
								corridor.walls(axis="x")
								matrix.glue(corridor, allowList)
								if x != matrix.width-1:
									print(y,x)
									r2id = self.collisionChecker((y,x), rooms)
									rooms[r2id].directions.remove("left")
								r.directions.remove("right")
								exitFlag = True
								break
						if exitFlag:
							break

				elif dir == "up":
					exitFlag = False
					for x in range(x0+1, x0+w-1):
						for j, y in enumerate(range(y0-1, -1, -1)):
							if y == 0:
								print("y000!!!!!111")
							if str(matrix[y][x]) in symbols or y == 0:
								
								corridor = Room(3, j+1, homogeneous=True, value="c", coordinates=[y+1, x-1])
								corridor.walls(axis="y")
								matrix.glue(corridor, allowList)
								print(matrix)
								if y != 0:
									print(y,x)
									r2id = self.collisionChecker((y,x), rooms)
									rooms[r2id].directions.remove("down")
								r.directions.remove("up")
								exitFlag = True
								break
						if exitFlag:
							break

				elif dir == "down":
					exitFlag = False
					for x in range(x0+1, x0+w-1):
						for j, y in enumerate(range(y0+h, matrix.height)):
							if y == matrix.height:
								print("y==matrix.height!!!!!!!!!!!")
							if str(matrix[y][x]) in symbols or y == matrix.height-1:
								
								corridor = Room(3, j+1, homogeneous=True, value="c", coordinates=[y0+h-1, x-1])
								corridor.walls(axis="y")
								matrix.glue(corridor, allowList)
								print(matrix)
								if y != matrix.height-1:
									print(y,x)
									r2id = self.collisionChecker((y,x), rooms)
									rooms[r2id].directions.remove("up")
								r.directions.remove("down")
								exitFlag = True
								break
						if exitFlag:
							break
				
		return corridors

	def impositionChecker(self, i, rooms):
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

	def collisionChecker(self, coordinates, rooms):
		y, x = coordinates
		for rid, room in enumerate(rooms):
			y2, x2 = room.coordinates
			h2, w2 = room.height, room.width
			if y in (y2, y2+h2-1):
				if x2 <= x <= x2+w2-1:
					return rid
			elif x in (x2, x2+w2-1):
				if y2 <= y <= y2+h2-1:
					return rid

	def roomChecker(self, rm, i, rooms, matrix):
		y1, x1 = rm.coordinates
		h1, w1 = rm.height, rm.width

		if (y1 == 0 or x1 == 0 or
			y1 + h1 == matrix.height or
			x1 + w1 == matrix.width):
			rm.canExpand = False
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
						return True

				if (x1 <= x2 + w2 - 1 and
					x1 + w1 - 1 >= x2):
					if (y1 + h1 == y2 or
						y1 == y2 + h2):
						rm.canExpand = False
						room.canExpand = False
						return True


	'''def filter(self, matrix, width, height):
		for i in range(height):
			for j in range(width):
				if matrix[i][j] == "#":
					matrix[i][j] = 2
				elif str(matrix[i][j]) in "./^<—+|\\>L?-*:JZxbMc":
					matrix[i][j] = 1
				
		return matrix'''
