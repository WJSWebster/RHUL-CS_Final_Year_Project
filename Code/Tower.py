import pygame

class Tower:
	def __init__(self, x, y, hover):
		self.x = x
		self.y = y
		self.size = 28
		self.hover = hover

	def render(self):
		if self.hover:
			# background = pygame.Display.set_mode()
			tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01_Transparent.png")
			#  pygame.mouse.set_visible(False)
			#  pygame.mouse.set_cursor  # https://www.pygame.org/docs/ref/mouse.html#pygame.mouse.set_cursor
		else:
			# if 'target_creep' is right of tower: use "Tower01_E.png", etc...
			tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01.png")

		tower_Img = pygame.transform.scale(tower_Img, (self.size, self.size))
		surface.blit(tower_Img, (self.x, self.y))
