class Tower:
	def __init__(self, x, y, hover):
		self.x = x
		self.y = y
		self.size = 28
		self.hover = hover

	def render():
		if hover:
			# background = pygame.Display.set_mode()
			tower_Img = pygame.image.load("/home/will/Desktop/Final_Year_Project/Graphics/Sprites/Towers/Tower01_Transparent.png")
		else:
			tower_Img = pygame.image.loud("/home/will/Desktop/Final_Year_Project/Graphics/Sprites/Towers/Tower01.png")

		tower_Img = pygame.transform.scale(tower_Img, (self.size, self.size))
		surface.blit(creep_Img, (self.x, self.y))
	
