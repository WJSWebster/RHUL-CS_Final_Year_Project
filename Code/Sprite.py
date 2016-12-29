import pygame

class Sprite:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

		self.size = 28
		self.direction = 'WEST'

		self.flagNo = 0
		self.pathComplete = False

	def render(self):
		if self.direction == 'WEST':
			creep_Img = pygame.image.load("Graphics/Sprites/Creeps/Creep01_W.png")
		elif self.direction == 'NORTH':
			creep_Img = pygame.image.load("Graphics/Sprites/Creeps/Creep01_N.png")
		elif self.direction == 'SOUTH':
			creep_Img = pygame.image.load("Graphics/Sprites/Creeps/Creep01_S.png")
		elif self.direction == 'EAST':
			creep_Img = pygame.image.load("Graphics/Sprites/Creeps/Creep01_E.png")

		creep_Img = pygame.transform.scale(creep_Img, (self.size, self.size))
		surface.blit(creep_Img, (self.x, self.y))
		#  pygame.draw.rect(surface, red, (self.x, self.y, self.width, self.height))

def placeTower():
	new_Tower = Tower(mouse[0], mouse[1], True)
	return new_Tower
