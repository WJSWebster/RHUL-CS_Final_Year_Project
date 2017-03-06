class Sprite:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

		self.size = 28
		self.direction = 'West'

		self.flagNo = 0
		self.pathComplete = False

		self.health = 10  # this is the default for the example sprite atm

		self.attackDamage = 2 # again, a default stat for now...
		self.attackFrameCount = 0
		self.attackSpeed = 30  # the number of frames before creep can attack again

	def creepPathFollow(self, flagCoords):
		if self.flagNo == len(flagCoords):
			print self, ": Complete"
			self.pathComplete = True
		else:
			if (flagCoords[self.flagNo][0] + 0.5) > self.x > (flagCoords[self.flagNo][0] - 0.5) and (flagCoords[self.flagNo][1] + 0.5) > self.y > (flagCoords[self.flagNo][1] - 0.5):
				self.flagNo += 1
				print self, " flagNo = ", self.flagNo
			else:
				if not (flagCoords[self.flagNo][0] + 0.5) > self.x > (flagCoords[self.flagNo][0] - 0.5):
					if self.x < flagCoords[self.flagNo][0]:
						self.direction = 'East'
						self.x += creep_Speed
						# print self.x, " < ", flagCoords[flagNo][0]
					elif self.x > flagCoords[self.flagNo][0]:
						self.direction = 'West'
						self.x -= creep_Speed
						# print self.x, " > ", flagCoords[flagNo][0]
				elif not (flagCoords[self.flagNo][1] + 0.5) > self.y > (flagCoords[self.flagNo][1] - 0.5):
					if self.y < flagCoords[self.flagNo][1] + 0.5:
						self.direction = 'South'
						self.y += creep_Speed
					elif self.y > flagCoords[self.flagNo][1]:
						self.direction = 'North'
						self.y -= creep_Speed
			# print "x = ", self.x, ", y = ", self.y

	def attacked(self, damage):
		self.health = self.health - damage
		print self, " health = ", self.health
		creepHealthCheck(self)

	def attackCheck(self):
		global heartHealth
		if self.attackFrameCount == self.attackSpeed:
			# play attack animation - would have to be a loop in of itself
			heartHealth = heartHealth - self.attackDamage
			self.attackFrameCount = 0
		else:
			self.attackFrameCount = self.attackFrameCount + 1

	def render(self):
		creep_Img = pygame.image.load("Graphics/Sprites/Creeps/Creep01_%s.png" % (self.direction))
		creep_Img = pygame.transform.scale(creep_Img, (self.size, self.size))
		surface.blit(creep_Img, (self.x, self.y))
		#  pygame.draw.rect(surface, red, (self.x, self.y, self.width, self.height))
