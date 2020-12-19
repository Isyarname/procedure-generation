import pygame as p
from matrix_reload import *
from ProcedureGeneration import Planning, BSPTree

#pl = Planning()
bsp = BSPTree()
width, height = 50,25
m = Matrix()

p.init()
tileSize = 15
surf = p.display.set_mode((width*tileSize, height*tileSize))
surfTile = p.Surface((tileSize, tileSize))

locations = {
	0:"sprites/void.png",
	1:"sprites/empty_space.png",
	2:"sprites/wall.png"
}

def drawDungeon(m):
	for i in range(height):
		for j in range(width):
			tile = p.image.load(locations[m[i][j]])
			surf.blit(tile, (tileSize*j, tileSize*i))

def generateDungeon():
	#dungeon = pl.generate(width=width, height=height, numberOfRooms=6, depth=5, numberOfExits=1)
	dungeon = bsp.generate(width=width, height=height, numberOfExits=1)
	m = dungeon.body
	drawDungeon(m)
	print(len(m), len(m[0]))
	
generateDungeon()

while True:
	for event in p.event.get():
		if event.type == p.QUIT:
			exit()
			sys.exit()
		elif event.type == p.KEYDOWN:
			if event.key == p.K_SPACE:
				generateDungeon()
			elif event.key == p.K_UP:
				p.image.save(surf, "dungeon.png") 

	p.display.update()