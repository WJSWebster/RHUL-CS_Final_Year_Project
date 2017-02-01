#from Sprite import *  # cannot render because makes calls to 'surface'
#from Tower import *
#import __ini__
import pygame, math, random, sys

# Global variables for now:
canvas_width = 1000
canvas_height = 800

map_Size = ((1760 / 2.2), (1440 / 2.2))
map_Coords = (20, 140)
map_Entrance = ((map_Size[0] + map_Coords[0]),(((map_Size[1] + map_Coords[1]) / 2) + 12))  # temporary - depends on map type

pygame.init()

mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed()

largeText = pygame.font.SysFont('ubuntu', 80)  # 'ubuntu'
smallText = pygame.font.SysFont('ubuntu', 20)  # 'ubuntu'

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)
red = (200, 0, 0)
bright_red = (255, 0, 0)
orange = (227, 150, 0)
bright_orange = (255, 165, 0)
map_green = (70, 147, 65)
map_yellow = (249, 170, 10)
map_grey = (135, 135, 135)


button_State = 0

# these all need to be moved to within game method
creep_List = []
creep_Speed = 1  # temporary - later refer to "bible"
tower_List = []
grid_List = []

heartHealth = 20

# rendering 'canvas':
canvas_dimensions = (canvas_width, canvas_height)
surface = pygame.display.set_mode(canvas_dimensions)

deltaTime = 0
getTicksLastTime = 0

def text_objects(text, font, colour):  # why font?
	textSurface = font.render(text, True, colour)
	return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, colour, action=None):  # change variable names
	global button_State
	mouse = pygame.mouse.get_pos()   # needs to be re-defined every loop to update
	click = pygame.mouse.get_pressed()   # " "

	"""
	if click[0] == 1:
		print "mouse position: ", mouse
	"""

	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		button = pygame.image.load("Graphics/Sprites/Buttons/%s_Highlighted.png" % (colour))
		if click[0] == 1:
			button = pygame.image.load("Graphics/Sprites/Buttons/%s_Pressed.png" % (colour))
			button_State = 1
		if button_State == 1 and click[0] == 0:  # 'action() is not None' = legacy code
		#event.type == pygame.MOUSEBUTTONUP
			button_State = 0
			action()

	else:
		button = pygame.image.load("Graphics/Sprites/Buttons/%s.png" % (colour))

	button = pygame.transform.scale(button, (w, h))
	surface.blit(button, (x, y))

	textSurf, textRect = text_objects(msg, smallText, white)
	textRect.center = ((x + (w / 2)), (y + (h / 2)))
	surface.blit(textSurf, textRect)  # need to blit every time rendering a new element


def intro_menu():
	pygame.display.set_caption("Will's TD Game -- Menu")
	pygame_quit = True  # this is a weird debug solution because otherwise 'pygame_quit' is undeclared
	#  while menu:
	surface.fill(white)

	menuBackground = pygame.image.load("Graphics/Background/Main_Background.png")  # OG size = '1760 x 1440'
	surface.blit(menuBackground, (0, 0))


	TextSurf, TextRect = text_objects("Game Title", largeText, white)
	TextRect.center = ((canvas_width / 2), (canvas_height / 3))
	surface.blit(TextSurf, TextRect)

	beginButtonYPos = (canvas_width / 3)
	makeButtonYPos = (canvas_width / 2)
	quitButtonYPos = (beginButtonYPos * 2)

	while (True):  # debug: creates an infinite loop, so window doesnt immediately close!
		button("Begin", beginButtonYPos, 450, 100, 50, "Blue", main)
		button("Make Map", makeButtonYPos, 450, 150, 50, "Orange", makeMap)
		button("Quit", quitButtonYPos, 450, 100, 50, "Red", pygame_quit)

		pass
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame_quit()
		pygame.display.flip()  # "Ok Pygame, now do your thang" - basically the same as pygame.display.update()


def main():
	pygame.display.set_caption("Will's TD Game -- Game")

	# is any of this stuff necessary???
	# rendering 'canvas':
	canvas_dimensions = (canvas_width, canvas_height)
	surface = pygame.display.set_mode(canvas_dimensions)
	surface.fill(white)

	# rendering background image
	background_Img = pygame.image.load("Graphics/Background/Game_Background.png")

	# loading temp map background
	temp_MapImg = pygame.image.load("Graphics/Background/Template(22x18).jpg")  # OG size = '1760 x 1440'
	temp_MapImg = pygame.transform.scale(temp_MapImg, (int(map_Size[0]), int(map_Size[1])))
	# should probs implement a 'try:, except: ' for each image render

	"""
	flagCoords = getFlagCoords()
	flag_Size = 30
	# spawning checkpoint flags on mapFlags
	checkpointFlag_Img = pygame.image.load("Graphics/checkpointFlag.jpg")
	checkpointFlag_Img = pygame.transform.scale(checkpointFlag_Img, (flag_Size, flag_Size))
	"""

	while (True):  # debug: creates an infinite loop, so window doesnt immediately close!
		mouse = pygame.mouse.get_pos()   # needs to be re-defined every loop to update
		click = pygame.mouse.get_pressed()   # " "

		surface.blit(background_Img, (0, 0))

		button("Menu", 50, 50, 100, 50, "Blue", intro_menu)
		towerCreated = button("Spawn tower", 200, 50, 200, 50, "Orange", placeTower)
		button("Spawn creep", 450, 50, 150, 50, "Red", addCreep)

		surface.blit(temp_MapImg, map_Coords)

		if heartHealth <= 0:
			TextSurf, TextRect = text_objects("Game Over", largeText, red)
			TextRect.center = (canvas_width/2, canvas_height/2)
			surface.blit(TextSurf, TextRect)
		else:
			TextSurf, TextRect = text_objects(("Heart Health: %s" % heartHealth), smallText, white)
			TextRect.center = (150, 600)
			surface.blit(TextSurf, TextRect)

		"""
		# DEBUG
		# blit flags on map
		for i in flagCoords:
			mapFlag_CoordX, mapFlag_CoordY = i
			surface.blit(checkpointFlag_Img, ((mapFlag_CoordX), (mapFlag_CoordY)))
		"""

		for i in tower_List:
			if i.hover:
				i.x, i.y = mouse
				if click[0] == 1 and (map_Coords[0] <= mouse[0] <= (map_Coords[0] + map_Size[0])) and (map_Coords[1] <= mouse[1] <= (map_Coords[1] + map_Size[1])):
					i.hover = False
					pygame.mouse.set_visible(True)
			i.render()

		for i in creep_List:
			if not creepHealthCheck(i):
				if not i.pathComplete:
					i.creepPathFollow(flagCoords)
				else:
					i.attackCheck()
				i.render()

		"""
		# trying to implemenet a delta time such that game loops consistently with frame rate (https://goo.gl/Pfmrx5)
		global deltaTime
		global getTicksLastFrame

		t = pygame.time.get_ticks()
		# deltaTime in seconds.
		getTicksLastFrame = t
		deltaTime = (t - getTicksLastFrame) / 1000.0
		print deltaTime
		"""

		pass
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame_quit()
		pygame.display.flip()  # basically the same as pygame.display.update()

def makeMap():
	pygame.display.set_caption("Will's TD Game -- Map Editor")

	surface.fill(map_grey)
	# loading temp map background
	temp_MapImg = pygame.image.load("Graphics/Background/Template(22x18).jpg")  # OG size = '1760 x 1440'
	temp_MapImg = pygame.transform.scale(temp_MapImg, (int(map_Size[0]), int(map_Size[1])))

	index = 0
	for yi in range(18):
		for xi in range(22):
			new_Grid = Grid(index, xi, yi)
			grid_List.append(new_Grid)
			index = index + 1

	selectedColour = None

	while (True):  # debug: creates an infinite loop, so window doesnt immediately close!
		print "new", selectedColour
		mouse = pygame.mouse.get_pos()   # needs to be re-defined every loop to update
		click = pygame.mouse.get_pressed()

		button("Menu", 50, 50, 100, 50, "Blue", intro_menu)
		button("(Save)", 200, 50, 100, 50, "Blue")  # not yet implemented
		button("Spawn creep", 450, 50, 150, 50, "Red", addCreep)

		TextSurf, TextRect = text_objects("Map drawing:", smallText, white)
		TextRect.center = (902, 177)
		surface.blit(TextSurf, TextRect)

		colourButtonSize = 32
		selectedColour = colourSelect(map_green, 902, 237, colourButtonSize, selectedColour)
		selectedColour = colourSelect(map_yellow, 902, 297, colourButtonSize, selectedColour)
		#greyPos = 902, 357  # this function will be a little different
		print selectedColour
		if selectedColour != None:
			colourPainter(grid_List, selectedColour)

		surface.blit(temp_MapImg, map_Coords)

		pathTesting = False  # for now

		for i in grid_List:
			if pathTesting:
				if i.colour in (map_yellow, red) and not checkNeighbours(i):
					i.colour = red
					print "ERROR: path not connected at point ", i.xi + 1, ", ", i.yi +1
				elif i.colour in (map_yellow, red) and checkNeighbours(i):
					i.colour = map_yellow
			#else:
			#	i.colour = map_green
			i.render()

		pass
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame_quit()
		pygame.display.flip()  # basically the same as pygame.display.update()

def colourSelect(colour, x, y, size, previousColour):
	global button_State
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	pygame.draw.rect(surface, colour, (x, y, size, size))
	#rect.center = (x, y)

	#if x + (size/2) > mouse[0] > x - (size/2) and y + (size/2) > mouse[1] > y - (size/2):  # if centered
	if x <= mouse[0] < x + size and y <= mouse[1] < y + size:
		#highlighted
		if click[0] == 1:
			#pressed
			button_State = 1
		if button_State == 1 and click[0] == 0:
			button_State = 0
			return colour
	return previousColour

def colourPainter(grid_List, colour):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if click[0] == 1 and (map_Coords[0] <= mouse[0] <= (map_Coords[0] + map_Size[0])) and (map_Coords[1] <= mouse[1] <= (map_Coords[1] + map_Size[1])):
		print "in grid click"
		for i in grid_List:
			if i.x <= mouse[0] < i.x + i.size and i.y <= mouse[1] < i.y + i.size:
				i.colour = colour
				print i

def checkNeighbours(i):
	connections = 0
	if grid_List[i.number-22].colour in (map_yellow, red):
		connections = connections + 1
	if grid_List[i.number+22].colour in (map_yellow, red):
		connections = connections + 1
	if grid_List[i.number-1].colour in (map_yellow, red):
		connections = connections + 1
	if grid_List[i.number+2].colour in (map_yellow, red):
		connections = connections + 1

	if connections != 2:
		return False
	else:
		return True

def getFlagCoords(mapName = "Main"):  # again, only if input argument is blank (for now)
	# "IF mapname = temp_MapIMG: " for example
	# in later implementations consider json.load(file) to load creep flag coords from txt file
	# mapFlags = [(15, 8), (15, 3), (6, 3), (6, 10), (13, 10), (13, 16), (5, 16)]  # creates a list of tuples (cant be altered later) - this is only a temp variable
	mapFlags = None

	with open('MapFlagCoords.txt', 'r') as inputfile:
	#inputfile = open('MapFlagCoords.txt', 'r')
		# line = 0
		print inputfile.readline()
		for line in inputfile:
			print 1
			if "main" in line:
				print 2
				mapFlags = line.split('=')[1]

	print "mapFlags: ", mapFlags

	mapFlags = [(15, 8), (15, 3), (6, 3), (6, 10), (13, 10), (13, 16), (5, 16)]  # creates a list of tuples (cant be altered later) - this is only a temp variable

	flagCoords = []
	for mx, my in mapFlags:
		flagCoords.append(((((mx - 1) * 80 / 2.2) + map_Coords[0]), (((my - 1) * 80 / 2.2) + map_Coords[1])))  # note: this may be problematic if x or y = 1?
	return flagCoords

def addCreep():
	new_Creep = Sprite(map_Entrance[0], (map_Entrance[1] - 15))  # - 15 so top left corner of pre-entrance tile
	creep_List.append(new_Creep)

def creepHealthCheck(creep):
	if creep.health == 0:
		creepIndex = creep_List.index(creep)
		print creep, "Died"
		creep_List.pop(creepIndex)
		return True
	else:
		return False


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

def placeTower():
	new_Tower = Tower(mouse[0], mouse[1], True)
	tower_List.append(new_Tower)

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

class Grid:
	def __init__ (self, number, xi, yi):
		self.number = number
		#print self.number
		self.xi = xi  # 0 - 21
		self.yi = yi  # 0 - 17

		self.size = 36.5

		self.x = (xi * self.size) + map_Coords[0]
		self.y = (yi * self.size) + map_Coords[1]


		self.colour = map_green

	def checkNeighbours():
		# maybe want to do this in each loop of makeMap
		print""

	def render(self):
		pygame.draw.rect(surface, self.colour, (self.x, self.y, self.size, self.size))


if __name__ == "__main__":  # https://goo.gl/1CRvRx & https://goo.gl/xF4xOF
	intro_menu()
	#  main()
	#  pygame_quit()  # will this work? or will it need to be included in each "stage" function?


def pygame_quit():
	pygame.quit()
	#  sys.exit(0)
	quit()

"""
def pygame_resize():  # not yet properly implemented: http://pygame.org/wiki/WindowResizing?parent=
	if event.type == VIDEORESIZE:
		screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
		screen.blit(pygame.transform.scale(pic, event.dict['size']),(0,0))
        pygame.display.flip(
"""
