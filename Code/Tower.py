class Tower:
	def __init__(self, x, y, hover):
		self.x = x
		self.y = y

		self.size = 28
		# self.target = creep_List[0]
		self.direction = "None"
		self.hover = hover

		self.damage = 2 # again, a default stat for now...

		self.attacking = False
		self.attackSpeed = 120  # dependent on tower
		self.attackFrameCount = 0
		self.target = None
		self.targetXInitial = None
		self.targetYInitial = None
		self.shadow_Img = pygame.transform.scale(pygame.image.load("Graphics/Sprites/Other/Shadow.png"), (self.size, self.size))
		self.explosion_Img = pygame.transform.scale(pygame.image.load("Graphics/Sprites/Other/Explosion.png"), (self.size, self.size))

	def targetFinder(self):
		if not self.attacking:  # wont even be tested unless attacking is False (pointless?)
			if len(creep_List) != 0:
				self.target = creep_List[0]
				return True
			else:
				return False
		# note: creep_List[0] means that the target is always the one at the front

		"""
		# if target is within range: " ", else self.direction = "None"
		if target.x > self.x:
			self.direction = "North"
		elif target.x < self.x:
			self.direction = "South"
		if target.y > self.y:
			self.direction = "East"
		elif target.y < self.y:
			self.direction = "West"
		# need a section to account for creep speed, time of projectile and possible corners
		"""

	def cannonBallAttack(self):
		if not self.attacking:
			if self.targetFinder():
				self.targetXInitial, self.targetYInitial = self.target.x, self.target.y
				self.attacking = True
		else:
			if self.attackFrameCount == self.attackSpeed:
				surface.blit(self.explosion_Img, (self.targetXInitial, self.targetYInitial))
				self.target.attacked(self.damage)
				self.attacking = False
				self.target, self.targetXInitial, self.targetYInitial = None, None, None
				self.attackFrameCount = 0
			else:
				self.attackFrameCount = self.attackFrameCount + 1
				surface.blit(self.shadow_Img, (self.targetXInitial, self.targetYInitial))

	def render(self):
		if self.hover:
			# background = pygame.Display.set_mode()
			tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01_Transparent.png")
			pygame.mouse.set_visible(False)
			#  pygame.mouse.set_cursor  # https://www.pygame.org/docs/ref/mouse.html#pygame.mouse.set_cursor
		else:
			self.cannonBallAttack()
			if self.direction == "None":
				tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01.png")
			else:
				tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01_%s.png" % (self.direction))

		tower_Img = pygame.transform.scale(tower_Img, (self.size, self.size))
		surface.blit(tower_Img, (self.x, self.y))

		if not self.hover:
			self.cannonBallAttack()
