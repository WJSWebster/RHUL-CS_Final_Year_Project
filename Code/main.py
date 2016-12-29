from Sprite import *  # cannot render because makes calls to 'surface'
from Tower import *
import pygame, math, random, sys

# Global variables for now:
canvas_width = 1000
canvas_height = 800

map_Size = (1760, 1440)
map_Coords = (20, 140)
map_Entrance = (((map_Size[0] / 2.2) + map_Coords[0]), ((((map_Size[1] / 2.2) / 2) + map_Coords[1]) - 53))

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


creep_Count = 1  # debug - will initialise 0
# OR:   (investigate)
creep_List = []


creep_Speed = 1  # temporary - later refer to "bible"
hovering = False  # another temp value, while trying to figure out best stratergy for spawning in towers.

# rendering 'canvas':
canvas_dimensions = (canvas_width, canvas_height)
surface = pygame.display.set_mode(canvas_dimensions)

deltaTime = 0
getTicksLastTime = 0

def text_objects(text, font, colour):  # why font?
	textSurface = font.render(text, True, colour)
	return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, colour, action=None):  # change variable names
	mouse = pygame.mouse.get_pos()   # needs to be re-defined every loop to update
	click = pygame.mouse.get_pressed()   # " "

	#if click[0] == 1:
		#print "mouse position: ", mouse

	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		button = pygame.image.load("Graphics/Sprites/Buttons/%s_Highlighted.png" % (colour))
		if click[0] == 1:
			button = pygame.image.load("Graphics/Sprites/Buttons/%s_Pressed.png" % (colour))
			if action() is not None and event.type == pygame.MOUSEBUTTONUP:
				action()
			if action == "placeTower" and event.type == pygame.MOUSEBUTTONUP:
				return True

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
	quitButtonYPos = (beginButtonYPos * 2)

	while (True):  # debug: creates an infinite loop, so window doesnt immediately close!
		button("Begin", beginButtonYPos, 450, 100, 50, "Blue", main)
		button("Quit", quitButtonYPos, 450, 100, 50, "Red", pygame_quit)

		pass
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame_quit()
		pygame.display.flip()  # "Ok Pygame, now do your thang" - basically the same as pygame.display.update()


def main():
	pygame.display.set_caption("Will's TD Game -- Game")

	global deltaTime
	global getTicksLastFrame
	global hovering

	# is any of this stuff necessary???
	# rendering 'canvas':
	canvas_dimensions = (canvas_width, canvas_height)
	surface = pygame.display.set_mode(canvas_dimensions)
	surface.fill(white)

	# rendering background image
	background_Img = pygame.image.load("Graphics/Background/Game_Background.png")

	# loading temp map background
	temp_MapImg = pygame.image.load("Graphics/Background/Template(22x18).jpg")  # OG size = '1760 x 1440'
	temp_MapImg = pygame.transform.scale(temp_MapImg, (int(map_Size[0] / 2.2), int(map_Size[1] / 2.2)))
	# should probs implement a 'try:, except: ' for each image render

	# creating and adding initial creep object
	# initial_creep = Sprite(map_Entrance[0], (map_Entrance[1] - 15))  # - 15 so top left corner of pre-entrance tile
	# creep_List.append(initial_creep)

	flagCoords = getFlagCoords()
	flag_Size = 30

	# spawning checkpoint flags on mapFlags
	checkpointFlag_Img = pygame.image.load("Graphics/checkpointFlag.jpg")
	checkpointFlag_Img = pygame.transform.scale(checkpointFlag_Img, (flag_Size, flag_Size))

	while (True):  # debug: creates an infinite loop, so window doesnt immediately close!

		surface.blit(background_Img, (0, 0))

		button("Menu", 50, 50, 100, 50, "Blue", intro_menu)
		#  button("Spawn creep", 200, 50, 250, 50, red, bright_red
		towerCreated = button("Spawn tower", 200, 50, 200, 50, "Orange", "placeTower")
		button("Spawn creep", 450, 50, 150, 50, "Red", addCreep)

		surface.blit(temp_MapImg, map_Coords)

		"""
		# DEBUG
		# blit flags on map
		for i in flagCoords:
			mapFlag_CoordX, mapFlag_CoordY = i
			surface.blit(checkpointFlag_Img, ((mapFlag_CoordX), (mapFlag_CoordY)))
		"""

		# note: this is bullshit - CORRECT
		if towerCreated:
			test_tower = placeTower()
			towerCreated = False
		if 'test_tower' in locals():
			if test_tower.hover:
				test_tower.x, test_tower.y = mouse
				if click[0] == 1:
					test_tower.hover = False
					pygame.mouse.set_visible(True)
			print test_tower.hover
			test_tower.render()

		"""
		# trying to implemenet a delta time such that game loops consistently with frame rate (https://goo.gl/Pfmrx5)
		t = pygame.time.get_ticks()
		# deltaTime in seconds.
		getTicksLastFrame = t
		deltaTime = (t - getTicksLastFrame) / 1000.0
		# print deltaTime
		"""

		for i in creep_List:
			# creep pathfinding
			if not i.pathComplete:
				i.creepPathFollow(flagCoords)
				i.render()

		pass
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame_quit()
		pygame.display.flip()  # basically the same as pygame.display.update()

def getFlagCoords():
	# "IF mapname = temp_MapIMG: " for example
	# in later implementations consider json.load(file) to load creep flag coords from txt file
	mapFlags = [(15, 8), (15, 3), (6, 3), (6, 10), (13, 10), (13, 16), (5, 16)]  # creates a list of tuples (cant be altered later) - this is only a temp variable

	flagCoords = []
	for mx, my in mapFlags:
		flagCoords.append(((((mx - 1) * 80 / 2.2) + map_Coords[0]), (((my - 1) * 80 / 2.2) + map_Coords[1])))  # note: this may be problematic if x or y = 1?
	return flagCoords

def addCreep():
	new_Creep = Sprite(map_Entrance[0], (map_Entrance[1] - 15))  # - 15 so top left corner of pre-entrance tile
	creep_List.append(new_Creep)

class Sprite:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

		self.size = 28
		self.direction = 'WEST'

		self.flagNo = 0
		self.pathComplete = False

	def creepPathFollow(self, flagCoords):
		if self.flagNo == len(flagCoords) + 1:
			print self, ": Complete"
			self.pathComplete = True
		else:
			if (flagCoords[self.flagNo][0] + 0.5) > self.x > (flagCoords[self.flagNo][0] - 0.5) and (flagCoords[self.flagNo][1] + 0.5) > self.y > (flagCoords[self.flagNo][1] - 0.5):
				self.flagNo += 1
				print "flagNo = ", self.flagNo
			else:
				if not (flagCoords[self.flagNo][0] + 0.5) > self.x > (flagCoords[self.flagNo][0] - 0.5):
					if self.x < flagCoords[self.flagNo][0]:
						self.direction = 'EAST'
						self.x += creep_Speed
						# print self.x, " < ", flagCoords[flagNo][0]
					elif self.x > flagCoords[self.flagNo][0]:
						self.direction = 'WEST'
						self.x -= creep_Speed
						# print self.x, " > ", flagCoords[flagNo][0]
				elif not (flagCoords[self.flagNo][1] + 0.5) > self.y > (flagCoords[self.flagNo][1] - 0.5):
					if self.y < flagCoords[self.flagNo][1] + 0.5:
						self.direction = 'SOUTH'
						self.y += creep_Speed
					elif self.y > flagCoords[self.flagNo][1]:
						self.direction = 'NORTH'
						self.y -= creep_Speed
			# print "x = ", self.x, ", y = ", self.y

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
	tower_List.append(new_Tower)

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
