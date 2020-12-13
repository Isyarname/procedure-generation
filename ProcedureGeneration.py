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

	def collisionChecker(self, coordinates, rooms):
		y, x = coordinates
		for rid, room in enumerate(rooms):
			y2, x2 = room.coordinates
			h2, w2 = room.height, room.width
			if y2 <= y <= y2+h2-1:
				print("yyyyyyy")
				if x2 <= x <= x2+w2-1:
					print("yyyyyyy22222")
					return rid

	def corridorsCreator(self, rooms, matrix):
		#corridors = []
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
								#print(matrix)
								print("x", x)
								if x != 0 and matrix[y][x-1] != "c":
									print(y, x)
									r2id = self.collisionChecker((y,x), rooms)
									if r2id != None and "right" in rooms[r2id].directions:
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
								print("x",x)
								if x != matrix.width-1 and matrix[y][x+1] != "c":
									#print(y,x)
									r2id = self.collisionChecker((y,x), rooms)
									if r2id != None and "left" in rooms[r2id].directions:
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
								#print(matrix)
								print("y",y)
								if y != 0 and matrix[y-1][x] != "c":
									#print(y,x)
									r2id = self.collisionChecker((y,x), rooms)
									if r2id != None and "down" in rooms[r2id].directions:
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
								#print(matrix)
								print("y",y)
								if y != matrix.height-1 and matrix[y+1][x] != "c":
									#print(y,x)
									r2id = self.collisionChecker((y,x), rooms)
									if r2id != None and "up" in rooms[r2id].directions:
										rooms[r2id].directions.remove("up")
								r.directions.remove("down")
								exitFlag = True
								break
						if exitFlag:
							break
				
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
				ms.append(Room(width=tx, height=h, homogeneous=True, value=value, coordinates=[y, x]))
				ms.append(Room(width=h-tx, height=h, homogeneous=True, value=value+1, coordinates=[y, x+tx]))
			else:
				ty = randint(border, h-border)
				ms.append(Room(width=w, height=ty, homogeneous=True, value=value, coordinates=[y, x]))
				ms.append(Room(width=w, height=h-ty, homogeneous=True, value=value+1, coordinates=[y+ty, x]))
		elif h > w:
			ty = randint(border, h-border)
			ms.append(Room(width=w, height=ty, homogeneous=True, value=value, coordinates=[y, x]))
			ms.append(Room(width=w, height=h-ty, homogeneous=True, value=value+1, coordinates=[y+ty, x]))
		else:
			tx = randint(border, w-border)
			ms.append(Room(width=tx, height=h, homogeneous=True, value=value, coordinates=[y, x]))
			ms.append(Room(width=w-tx, height=h, homogeneous=True, value=value+1, coordinates=[y, x+tx]))

		return ms

	def split(self, matrix, border=4):
		ms = self.splitMatrix(matrix, 0, border)
		btb = matrix.width >= border*2 and matrix.height >= border*2
		count = 0
		if not btb:
			print("МАЛЕНЬКАЯ МАТРИЦАААААААААААА!!!!!!!!!!!")
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

	def smallerRooms(self, ms, halfDepth=2):
		ms2 = []
		for i in ms:
			print("i.coordinates[1]:",i.coordinates[1])
			print("i.width:", i.width)
			print("i.coordinates[0]:", i.coordinates[0])
			print("i.height:", i.height)
			y = randint(i.coordinates[0], i.coordinates[0]+i.height//2 - halfDepth)
			x = randint(i.coordinates[1], i.coordinates[1]+i.width//2 - halfDepth)
			x2 = randint(i.coordinates[1]+i.width//2 + halfDepth, i.coordinates[1]+i.width-1)
			y2 = randint(i.coordinates[0]+i.height//2 + halfDepth, i.coordinates[0]+i.height-1)
			w = x2 - x
			h = y2 - y
			ms2.append(Room(width=w, height=h, homogeneous=True, value=0, coordinates=[y, x]))
		return ms2

	def generate(self, height=30, width=30):
		border = 8
		matrix = Room(width, height, homogeneous=True, value=0)
		rooms = self.split(matrix, border)
		matrix.fill(0)
		rooms = self.smallerRooms(rooms, halfDepth=2)
		matrix.matrixJoiner(rooms)
		matrix = self.corridorsCreator(rooms, matrix)
		return self.filter(matrix, width, height)



class Planning(GenAlgorithm):
	def __init__(self):
		pass

	def generate(self, width=30, height=30, numberOfRooms=4, depth=5):
		if (height-1)//2 < depth > (width-1)//2:
			print("КОМНАТА НЕ ВЛЕЗЕТ В МАТРИЦУУУ!!!!!!!")
		else:
			matrix = Room(width, height, homogeneous=True, value=0)
			rooms = self.roomsCreator(width, height, numberOfRooms, depth)
			canExpand = True
			while canExpand:
				canExpand = False
				for i, r in enumerate(rooms):
					if rooms[i].canExpand:
						rooms[i].expand()
						self.roomChecker(rooms[i], i, rooms, matrix)
					canExpand = canExpand or rooms[i].canExpand
				matrix.matrixJoiner(rooms)
				print(matrix)
			matrix = self.corridorsCreator(rooms, matrix)
			print(self.filter(matrix, width, height))
			return self.filter(matrix, width, height)

	def roomsCreator(self, width, height, numberOfRooms, depth):
		rooms = []
		for i in range(numberOfRooms):
			r = Room(depth, depth, coordinates=[randint(depth,height-1-depth), randint(depth,width-1-depth)])
			rooms.append(r)
			while self.impositionChecker(i, rooms):
				rooms[i].coordinates = [randint(depth,height-1-depth), randint(depth,width-1-depth)]
		return rooms

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
