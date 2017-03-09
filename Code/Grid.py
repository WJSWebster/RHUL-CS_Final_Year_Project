import random, pygame
pygame.init()
from main import map_Coords, frameCounter, surface


map_green = (70, 147, 65)
map_yellow = (249, 170, 10)
map_grey = (135, 135, 135)
path_blue = (0, 191, 255)

class Grid:
	def __init__ (self, number, xi, yi, colour = map_green):

		self.number = number

		self.xi = xi  # 0 - 21
		self.yi = yi  # 0 - 17

		self.size = 36.5

		self.x = (xi * self.size) + map_Coords[0]
		self.y = (yi * self.size) + map_Coords[1]

		#self.direction = direction
		self.colour = colour
		self.randColour = []

		divergenceAmount = 6
		for i in colour:
			if bool(random.getrandbits(1)):
				randDivergence = i + random.randint(0,divergenceAmount)
			else:
				randDivergence = i - random.randint(0,divergenceAmount)
			self.randColour.append(randDivergence)



	def checkNeighbours():
		# maybe want to do this in each loop of makeMap
		pass

	def render(self): #, x = self.x, y = self.y, colour = self.colour
		if frameCounter == 1:  # ie, in map editor, not in game
			pygame.draw.rect(surface, self.colour, (self.x, self.y, self.size, self.size))
		else:
			pygame.draw.rect(surface, self.randColour, (self.x, self.y, self.size, self.size))
