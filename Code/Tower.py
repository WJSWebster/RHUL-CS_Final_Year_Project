from main import surface, entitySelected, creep_List
# import Creep
import pygame

class Tower(pygame.sprite.Sprite):
	def __init__(self, x, y, hover):
		from main import creep_List
		global creep_List
		pygame.sprite.Sprite.__init__(self)

		self.type = "Basic"  # for now, will be read in from text file
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
		self.shadow_Img = pygame.image.load("Graphics/Sprites/Other/Shadow.png").convert_alpha()
		self.cannonBall_Img = pygame.transform.scale(pygame.image.load("Graphics/Sprites/Other/CannonBall.png").convert_alpha(), (self.size, self.size))
		# self.explosion_Img = pygame.transform.scale(pygame.image.load("Graphics/Sprites/Other/Explosion.png").convert_alpha(), (self.size, self.size).convert())

		self.explosionSize = int(self.size * 2)
		self.aftermathFrameCount = 0
		self.aftermathXCoord = None
		self.aftermathYCoord = None
		self.aftermathBool = False

		print "__init__ creep_List:", creep_List


	def targetFinder(self):
		from main import creep_List
		global creep_List

		print "creep_List", creep_List

		print "finding target..."
		if not self.attacking:  # wont even be tested unless attacking is False (pointless?)
			print "im not attacking"
			if len(creep_List) != 0:
				print "creep_List[0]: ",creep_List[0]
				self.target = creep_List[0]
				print "target", self.target
				return True
			else:
				print "Falso"
				print "creep_List[0]", creep_List[0]
				return False
			print "help?~~~"
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
				print "Tower target:", self.target

				self.targetXInitial, self.targetYInitial = self.target.x, self.target.y
				self.attacking = True
				self.attackFrameCount = 1  # re-assigned at the beginning (maybe?)
		else:
			if self.attackFrameCount == self.attackSpeed:  # attack frame
				self.target.attacked(self.damage)
				self.cannonBallAftermath(self.targetXInitial, self.targetYInitial)
				self.attacking = False
				self.target, self.targetXInitial, self.targetYInitial = None, None, None
			elif self.attackFrameCount < self.attackSpeed:  # attack coming
				sizeMultiplied = int(self.size + (self.size - ((float(self.attackFrameCount) / self.attackSpeed) * self.size)))
				fallDistance = float((self.attackSpeed - self.attackFrameCount) / 0.25)

				shadow_Img = pygame.transform.scale(self.shadow_Img, (sizeMultiplied, sizeMultiplied))
				surface.blit(shadow_Img, (self.targetXInitial - (sizeMultiplied / 5), self.targetYInitial - (sizeMultiplied / 5)))
				surface.blit(self.cannonBall_Img, (self.targetXInitial, (self.targetYInitial - fallDistance)))
				self.attackFrameCount = self.attackFrameCount + 1

	def cannonBallAftermath(self, aftermathXCoord = None, aftermathYCoord = None):
		if aftermathXCoord != None and aftermathYCoord != None:  #new aftermath being initialised
			self.aftermathFrameCount = 1
			self.aftermathXCoord = aftermathXCoord
			self.aftermathYCoord = aftermathYCoord
			self.aftermathBool = True
		if self.aftermathFrameCount <= 35:  # during aftermath explosion  # 35 = self.aftermathFrameCount * 5
			explosion_Img = pygame.image.load("Graphics/Sprites/Explosions/Explosion_%s.png" % (int(self.aftermathFrameCount / 5))).convert_alpha()
			explosion_Img = pygame.transform.scale(explosion_Img, (self.explosionSize, self.explosionSize))
			surface.blit(explosion_Img, (self.aftermathXCoord - (self.explosionSize / 4), self.aftermathYCoord - (self.explosionSize / 4)))
			self.aftermathFrameCount = self.aftermathFrameCount + 1
		else:  # aftermath explosion ends
			self.aftermathBool = False
			self.aftermathXCoord = None  # back to __init__ state
			self.aftermathYCoord = None

	def render(self, xCoord = None, yCoord = None):
		if self.hover:
			# background = pygame.Display.set_mode()
			tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01_Transparent.png").convert_alpha()
			pygame.mouse.set_visible(False)
			#  pygame.mouse.set_cursor  # https://www.pygame.org/docs/ref/mouse.html#pygame.mouse.set_cursor
		else:
			#self.cannonBallAttack()
			if self.direction == "None":
				tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01.png").convert_alpha()
			else:
				tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01_%s.png" % (self.direction)).convert_alpha()

		tower_Img = pygame.transform.scale(tower_Img, (self.size, self.size))
		if xCoord == None and yCoord == None:  # rendering on game map
			surface.blit(tower_Img, (self.x, self.y))

			if entitySelected == self:
				silhouette_Img = pygame.image.load("Graphics/Sprites/Towers/TowerSilhouette.png").convert_alpha()
				silhouette_Img = pygame.transform.scale(silhouette_Img, (self.size, self.size))
				surface.blit(silhouette_Img, (self.x, self.y))

			if not self.hover:  # and if tower of type [1]
				self.cannonBallAttack()
		else:
			surface.blit(tower_Img, (xCoord, yCoord))
			if self.aftermathBool:
				self.cannonBallAftermath()
