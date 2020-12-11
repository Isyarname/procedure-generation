import pygame as p
from matrix_reload import *
from ProcedureGeneration import Planning

pl = Planning()
width, height = 30, 30
m = Matrix()

p.init()
surf = p.display.set_mode((width*20, height*20))
tileSize = 20
surfTile = p.Surface((20, 20))

locations = {
	0:"sprites/void.png",
	1:"sprites/empty_space.png",
	2:"sprites/wall.png"
}

def generateDungeon():
	dungeon = pl.generate()
	m = dungeon.body
	for i in range(width):
		for j in range(height):
			tile = p.image.load(locations[m[i][j]])
			surf.blit(tile, (tileSize*j, tileSize*i))
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