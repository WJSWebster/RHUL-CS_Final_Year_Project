import __init__
# import statement for Pygame, mathand sys libraries
import pygame, math, sys  # currently not using math

# Assigns the width and height of the screen as a tuple
canvas_width = 1000
canvas_height = 800
canvas_dimensions = (canvas_width, canvas_height)
surface = pygame.display.set_mode(canvas_dimensions)

# Assigns the dimensions and the top-left coordinates of the map
map_Size = ((1760 / 2.2), (1440 / 2.2))
map_Coords = (20, 140)

# Initialise Pygame
pygame.init()

# Manages how frequently surface updates ('flips')
clock = pygame.time.Clock()
fps = 60

# The location of the mouse cursor on screen and the state of each mouse button (re-assigned each loop)
mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed()

# Font styles for titles and regular text used when render/'displaying' text on screen
largeText = pygame.font.SysFont('ubuntu', 80)  # 'ubuntu'
smallText = pygame.font.SysFont('ubuntu', 20)  # 'ubuntu'

# 3 element tuples (representing RGB values respectively) of commonly used colours in the program
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
path_blue = (0, 191, 255)

# An integer of either 0 or 1, representing whether a menu button has been 'pressed' or not (such that action is only taken once button is 'un-pressed')
button_State = 0

# Default integers for the player's 'health' and 'budget' values and wave number the player is currently on for that map (re-assigned if save-data loaded)
playerHealth = 20
playerBudget = 0
waveNo = 1

# A list of all grid, creep and tower objects, respectively
grid_List = []
creep_List = []
tower_List = []
# A list to record the location and number of creep deaths during a game
death_List = []
# Represents what (single) object is 'highlighted' or selected by the player
entitySelected = None
# A string of the name of the map the player has chosen
mapSelection = ""
# A counter incrememnted each game loop, used to time creep spawn rate for each round
frameCounter = 1
# A list of tuples of the X and Y coordinates for each 'flag' that make up the path creeps must follow on a given map
flagCoords = []
# A seperate list of tuples used when referencing grid coordinates rather than 'real' X and Y coordinates (such as when loading flag coords from text file)
tempMapFlagCoords = []
# A tuple representing the starting X and Y coordinates of a creep upon creation
map_Entrance = ()
# A Boolean limiteding the player from saving an un-tested or unsuccessful map in the editor
testMapSuccessful = False

#creep_Speed = 1  # temporary - later refer to "Species.txt"

# Pygame image load function assignment for the main menu background image
menuBackground = pygame.image.load("Graphics/Background/Main_Background.png").convert()
# Pygame image load function assignment and further re-scaling for the grid overlay image
	#grid_OverlayImg = pygame.image.load("Graphics/Background/Grid_Overlay(Test).png")  # only used for debug
grid_OverlayImg = pygame.image.load("Graphics/Background/Grid_Overlay.png").convert_alpha()
grid_OverlayImg = pygame.transform.scale(grid_OverlayImg, (int(map_Size[0]), int(map_Size[1])))

deltaTime = 0
getTicksLastTime = 0

def resetGameState():
	global playerHealth, playerBudget, waveNo, grid_List, creep_List, tower_List, death_List, frameCounter, mapSelection, flagCoords, map_Entrance, entitySelected, testMapSuccessful

	playerHealth = 20
	playerBudget = 0
	waveNo = 1

	grid_List = []
	# generateGridList()
	creep_List = tower_List = death_List = []

	frameCounter = 1

	mapSelection = ""
	flagCoords = []
	map_Entrance = ()

	entitySelected = None

	testMapSuccessful = False

def displayText(text, font, colour, centX, centY):
	if "\n" in text:
		halfFontSize = font.get_linesize() / 2
		TextSurf, TextRect = text_objects(text.split('\n')[0], font, colour)
		TextRect.center = (centX, centY - halfFontSize)
		surface.blit(TextSurf, TextRect)

		TextSurf, TextRect = text_objects(text.split('\n')[1], font, colour)
		TextRect.center = (centX, centY + halfFontSize)
		surface.blit(TextSurf, TextRect)

	else:
		TextSurf, TextRect = text_objects(text, font, colour)
		TextRect.center = (centX, centY)
		surface.blit(TextSurf, TextRect)

def text_objects(text, font, colour):
	textSurface = font.render(text, True, colour)
	return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, colour, action = None, mapName = None):  # change variable names
	global button_State
	global mapSelection
	mouse = pygame.mouse.get_pos()   # needs to be re-defined every loop to update
	click = pygame.mouse.get_pressed()   # " "

	"""
	if click[0] == 1:
		print "mouse position: ", mouse
	"""

	if msg != "Save" and msg != "Delete": # and msg != "delete"
		if x + w > mouse[0] > x and y + h > mouse[1] > y:
			button = pygame.image.load("Graphics/Sprites/Buttons/%s_Highlighted.png" % (colour)).convert_alpha()  # currently within gameloop and as such, pulling image from mem very often (look to make gloal assignment)
			if click[0] == 1:
				button = pygame.image.load("Graphics/Sprites/Buttons/%s_Pressed.png" % (colour)).convert_alpha()
				button_State = 1
			if button_State == 1 and click[0] == 0:  # 'action() is not None' = legacy code
			#event.type == pygame.MOUSEBUTTONUP
				button_State = 0
				if action == intro_menu:
					resetGameState()
				if mapName != None:
					mapSelection = mapName.split(' ')[0]
					action()
				else:
					action()
		else:
			button = pygame.image.load("Graphics/Sprites/Buttons/%s.png" % (colour)).convert_alpha()
	else:
		button = pygame.image.load("Graphics/Sprites/Buttons/%s.png" % (colour)).convert_alpha()
		if x + w > mouse[0] > x and y + h > mouse[1] > y:
			if click[0] == 1:
				button_State = 1
			if button_State == 1 and click[0] == 0:
				button_State = 0
				action()  # either saveProgress() or deleteProgress()

	button = pygame.transform.scale(button, (w, h))
	surface.blit(button, (x, y))

	displayText(msg, smallText, white, (x + (w / 2)), (y + (h / 2)))

def saveProgress():
	global mapSelection
	mapName = ""
	mapFile = open("MapFlagCoords.txt", 'r')
	saveFile = open("Save.txt", 'r+')

	# first check that map saves match map_List
	for mapLine in mapFile:
		if "=[(" in mapLine:
			mapName = mapLine.split('=[')[0]
			for saveLine in saveFile:
				if ":" in saveLine:
					if mapName == saveLine.split(':')[0]:
						print mapName, "breaking"
						break
			else:
				print mapName, "not found in save file -- adding it now!"
				writeline = ("%s: \n") % (mapName)
				saveFile.write(writeline)
	mapFile.close()

	saveFile.seek(0)  # http://stackoverflow.com/questions/3906137/why-cant-i-call-read-twice-on-an-open-file
	lines = saveFile.read()
	saveFile.seek(0)

	for i, line in enumerate(saveFile):
		if ":" in line:
			if mapSelection == line.split(':')[0]:
				if i < len(lines):
					#if ":" in lines[i + 1]:
					if ":" in next(saveFile):
						print "there is nothing saved for this mapsave -- writing..."
						#writeline = ("- playerHealth = %s\n- tower_List = %s\n- waveNo = %s\n") % (playerHealth, tower_List, waveNo)
						#lines = lines.replace("%s: \n","%s: \n**test**\n")
						next_line = next(saveFile)
						print "next_line = ", next_line
						saveFile.write('**TEST**\n')
           				saveFile.write(next_line)
						#saveFile.write(lines)
						#writableLine = i + 1
						#print "i:", i, ", writableLine:", writableLine
					"""
					else:
						print "overwriting mapsave..."
					"""
				else:
					writeline = ("- playerHealth = %s\n- tower_List = %s\n- waveNo = %s\n") % (playerHealth, tower_List, waveNo)
					#writableLine = i
		#print i, "=", writableLine,"?", i == writableLine
		#if i == writableLine:
			#print "hello"
			#saveFile.write(writeline)
			#saveFile.write("test")

	if not saveFile.closed:
		print "file is still open"
		saveFile.close()
	#if saveFile.closed:
	#	print "file is closed"
	print "end2"

def loadProgress(mapName = mapSelection):
	if mapName != mapSelection:  #if an argument has been fed into function (ie, when pulling waveNo for buttons)
		waveSearchOnly = True
		mapWaveProgress = 0
	else:  #if loading progress upon entering a map
		waveSearchOnly = False
		global playerHealth
		global towerList
		global waveNo

	saveFile = open("Save.txt", 'r')
	searching = False

	for line in saveFile:
		if ":" in line:
			if mapName == line.split(':')[0]:
				searching = True
		if searching:
			if waveSearchOnly:
				if "waveNo" in line:
					return line.split("= ")[1]
			else:
				if "playerHealth" in line:
					playerHealth = line.split("= ")[1]
				if "tower_List" in line:
					towerList = line.split("= ")[1]
				if "waveNo" in line:
					waveNo = line.split("= ")[1]
			if ":" in line:
				searching = False

	saveFile.close()

def deleteProgress():
	pass

def intro_menu():
	pygame.display.set_caption("Will's TD Game -- Menu")
	pygame_quit = True  # this is a weird debug solution because otherwise 'pygame_quit' is undeclared
	#  while menu:
	surface.fill(white)
	surface.blit(menuBackground, (0, 0))

	displayText("Game Title", largeText, white, (canvas_width / 2), (canvas_height / 3))

	beginButtonXPos = (canvas_width / 3)
	makeButtonXPos = (canvas_width / 2) - 22
	quitButtonXPos = (beginButtonXPos * 2)
	# saveButtonXPos = (canvas_width - 200)
	deleteButtonxPos = (canvas_width - 100)

	while (True):  # debug: creates an infinite loop, so window doesnt immediately close!
		button("Begin", beginButtonXPos, 450, 100, 50, "Blue", mapSelect)
		button("Make Map", makeButtonXPos, 450, 150, 50, "Orange", makeMap)
		button("Quit", quitButtonXPos, 450, 100, 50, "Red", pygame_quit)
		#button("Save", saveButtonXPos, 50, 60, 60, "FloppyDisk", saveProgress)
		button("Delete", deleteButtonxPos, 50, 60, 60, "Cross", deleteProgress)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame_quit()

		# limits surface update rate to a maximum of 60 frames per second
		clock.tick(fps)
		# Pygame function to update surface with what has been blit-ed
		pygame.display.flip()

def mapSelect():
	pygame.display.set_caption("Will's TD Game -- Map Select")

	map_List = []
	difficulty = ""
	textFile = open("MapFlagCoords.txt", 'r')

	surface.fill(white)

	for line in textFile:
		if "=[(" in line:
			tupleNo = line.count("(")
			if tupleNo <= 10:
				difficulty = "Hard"
			elif tupleNo <= 20:
				difficulty = "Medium"
			else:
				difficulty = "Easy"
			#((waveNo/50)*100)
			map_List.append(line.split('=[')[0] + ("  [%s]\n(%s)" % (str(waveNo), str(difficulty))))

	textFile.close()
	while (True):
		surface.blit(menuBackground, (0, 0))

		for i in map_List:
			button(i, (canvas_width/2) - (150 / 2), (70 * (map_List.index(i) + 1)), 150, 50, "Blue", main, i)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame_quit()

		# limits surface update rate to a maximum of 60 frames per second
		clock.tick(fps)
		# Pygame function to update surface with what has been blit-ed
		pygame.display.flip()

def main():
	global map_Entrance, death_List, waveNo, frameCounter
	pygame.display.set_caption("Will's TD Game -- Game")

	# rendering 'canvas':
	surface.fill(white)

	# rendering background image
	background_Img = pygame.image.load("Graphics/Background/Game_Background.png").convert()

	"""
	# loading temp map background
	temp_MapImg = pygame.image.load("Graphics/Background/Template(22x18).jpg").convert()  # OG size = '1760 x 1440'
	temp_MapImg = pygame.transform.scale(temp_MapImg, (int(map_Size[0]), int(map_Size[1])))
	# should probs implement a 'try:, except: ' for each image render
	"""

	# getting flagCoords for map
	flagCoords = getFlagCoords()

	# filling death_List
	for i in flagCoords:
		death_List.append([flagCoords.index(i), 0])

	#print "death_List =", death_List
	map_Entrance = flagCoords[0]
	#print "map_Entrance = ", map_Entrance
	flag_Size = 30

	spawnList = []
	creepCount = 0

	"""
	# spawning checkpoint flags on mapFlags
	checkpointFlag_Img = pygame.image.load("Graphics/checkpointFlag.jpg").convert_alpha()
	checkpointFlag_Img = pygame.transform.scale(checkpointFlag_Img, (flag_Size, flag_Size))
	"""

	while (True):  # debug: creates an infinite loop, so window doesnt immediately close!
		mouse = pygame.mouse.get_pos()   # needs to be re-defined every loop to update
		click = pygame.mouse.get_pressed()   # " "

		surface.blit(background_Img, (0, 0))

		for i in grid_List:
			i.render()
		surface.blit(grid_OverlayImg, map_Coords)

		if playerHealth <= 0:
			healthColour = red
		else:
			healthColour = white

		towerCreated = button("Spawn tower", 200, 50, 200, 50, "Orange", placeTower)  # towerCreated legacy code, need to review
		button("Spawn creep", 450, 50, 150, 50, "Red", addCreep)
		button("Save", (canvas_width - 120), 50, 60, 60, "FloppyDisk", saveProgress)

		displayText("Your Health:\n%s" % (playerHealth), smallText, healthColour, (canvas_width - 320), 35)
		displayText("Creeps left:\n%s/%s" % ((len(spawnList) + len(creep_List)), creepCount), smallText, white, (canvas_width - 320), 90)

		displayText("Wave:\n%s" % (waveNo), smallText, white, (canvas_width - 220), 60)

		if playerHealth <= 0:
			pygame.draw.rect(surface, white, (0, 0, canvas_width, canvas_height))
			displayText("Game Over", largeText, red, canvas_width/2, canvas_height/2)
		button("Menu", 50, 50, 100, 50, "Blue", intro_menu)

		"""
		# DEBUG
		# blit flags on map
		for i in flagCoords:
			mapFlag_CoordX, mapFlag_CoordY = i
			surface.blit(checkpointFlag_Img, ((mapFlag_CoordX), (mapFlag_CoordY)))
		"""
		########################
		#####   Gameplay   #####
		########################
		if playerHealth > 0:
		# print "frameCounter = ", frameCounter

			if frameCounter == 1:
				spawnRate, creepCount, spawnList = getWaveInfo(waveNo)

			if frameCounter % spawnRate == 0:  # spawns a new creep from spawnList in accordance with spawnRate for that wave
				if len(spawnList) > 0:
					addCreep(spawnList[0])
					spawnList.pop(0)

			for i in tower_List:
				if i.hover:
					i.x, i.y = mouse
					if click[0] == 1 and (map_Coords[0] <= mouse[0] <= (map_Coords[0] + map_Size[0])) and (map_Coords[1] <= mouse[1] <= (map_Coords[1] + map_Size[1])):
						i.hover = False
						pygame.mouse.set_visible(True)
				else:
					checkSelected(mouse, click, i)
				i.render()

			for i in creep_List:
				if not creepHealthCheck(i):
					if not i.pathComplete:
						i.creepPathFollow(flagCoords)
						checkSelected(mouse, click, i)
						i.render()
					else:
						i.attackPlayer()


			if len(creep_List) == 0 and len(spawnList) == 0:
				print "creep_List & spawnList are empty!"
				waveNo = waveNo + 1
				frameCounter = 0

			"""
			if waveNo != 1:  # error checking
				print "waveNo =", waveNo
				print "frameCounter =", frameCounter
			"""

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

			frameCounter = frameCounter + 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:  # if window close button pressed
				pygame_quit()

		# limits surface update rate to a maximum of 60 frames per second
		clock.tick(fps)
		# Pygame function to update surface with what has been blit-ed
		pygame.display.flip()

def checkSelected(mouse, click, curEntity):
	global button_State, entitySelected
	dataXCoord = canvas_width - 90
	dataYCoord = 175  # initially, then incremented upon on future lines of data
	statsBackground = pygame.image.load("Graphics/Background/Stats_Background.png").convert_alpha()
	lineSize = smallText.get_linesize()
	lineIncrement = 1
	gridSize = 36.5

	if curEntity.x <= mouse[0] <= curEntity.x + curEntity.size and curEntity.y <= mouse[1] <= curEntity.y + curEntity.size: #and click[0] == 1:
		#highlighted
		if click[0] == 1:
			#pressed
			button_State = 1
		if click[0] == 0 and button_State == 1:
			button_State = 0
			if curEntity == entitySelected:
				entitySelected = None  # deselects entity
			else:
				entitySelected = curEntity
	if entitySelected == curEntity:
		if curEntity.__class__.__name__ == "Creep":  # if the object is a Creep class instance
			statsBackground = pygame.transform.scale(statsBackground, (150, 300))
			surface.blit(statsBackground, (dataXCoord - 75, dataYCoord - 40))

			displayText("Creep %s of %s:\n" % ((creep_List.index(curEntity) + 1), len(creep_List)), smallText, white, dataXCoord, dataYCoord + (lineSize * lineIncrement))
			lineIncrement = lineIncrement + 1

			#Grid.render(dataXCoord - (curEntity.size / 2), lineSize * lineIncrement, map_yellow)
			pygame.draw.rect(surface, map_yellow, (dataXCoord - (curEntity.size / 2), dataYCoord + (lineSize * lineIncrement), gridSize, gridSize))  #dataXCoord - (curEntity.size / 2)
			curEntity.render(dataXCoord - (curEntity.size / 2), dataYCoord + (lineSize * lineIncrement))
			lineIncrement = lineIncrement + 4

			attributeTuple = ('species', 'health', 'damage', 'speed', 'cost')
		else:  # object type == Tower
			statsBackground = pygame.transform.scale(statsBackground, (150, 280))
			surface.blit(statsBackground, (dataXCoord - 75, dataYCoord - 40))

			displayText("Tower %s of %s:\n" % ((tower_List.index(curEntity) + 1), len(tower_List)), smallText, white, dataXCoord, dataYCoord + (lineSize * lineIncrement))
			lineIncrement = lineIncrement + 1

			#Grid.render(dataXCoord - (curEntity.size / 2), lineSize * lineIncrement, map_greenw)
			pygame.draw.rect(surface, map_green, (dataXCoord - (curEntity.size / 2), dataYCoord + (lineSize * lineIncrement), gridSize, gridSize))
			curEntity.render(dataXCoord - (curEntity.size / 2), dataYCoord + (lineSize * lineIncrement))
			lineIncrement = lineIncrement + 4

			attributeTuple = ('type', 'damage', 'attackSpeed','target')

		for i in attributeTuple:
			for attr, value in curEntity.__dict__.iteritems():
				if i == attr:
					displayText("%s: %s\n" % (i.title(), value), smallText, white, dataXCoord, dataYCoord + (lineSize * lineIncrement))
					lineIncrement = lineIncrement + 1
					break


def makeMap():
	global frameCounter
	frameCounter = 1
	pygame.display.set_caption("Will's TD Game -- Map Editor")

	surface.fill(map_grey)

	generateGridList()

	selectedColour = None
	# testMapSuccessful = False

	while (True):  # debug: creates an infinite loop, so window doesnt immediately close!
		mouse = pygame.mouse.get_pos()   # needs to be re-defined every loop to update
		click = pygame.mouse.get_pressed()

		button("Menu", 50, 50, 100, 50, "Blue", intro_menu)
		if testMapSuccessful:
			button("(Save)", 200, 50, 100, 50, "Blue", saveMap)
			# button("Spawn creep", 550, 50, 150, 50, "Red", addCreep)
		else:
			button("(Save)", 200, 50, 100, 50, "Grey")
		button("Spawn creep", 550, 50, 150, 50, "Grey")  #not yet implemented
		button("Test", 400, 50, 100, 50, "Orange", testMap)

		displayText("Map drawing:", smallText, white, 902, 177)

		colourButtonSize = 32
		selectedColour = colourSelect(map_green, 902, 237, colourButtonSize, selectedColour)
		selectedColour = colourSelect(map_yellow, 902, 297, colourButtonSize, selectedColour)

		if selectedColour != None:
			colourPainter(selectedColour)

		"""
		surface.blit(temp_MapImg, map_Coords)  # not really needed, should really remove
		"""

		pathTesting()
		surface.blit(grid_OverlayImg, map_Coords)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:  # if window close button pressed
				pygame_quit()

		# limits surface update rate to a maximum of 60 frames per second
		clock.tick(fps)
		# Pygame function to update surface with what has been blit-ed
		pygame.display.flip()

def generateGridList(mapFlags = None):
	from Grid import Grid
	global grid_List

	gridNo = 0

	print mapFlags

	for yi in range(18):
		for xi in range(22):
			if mapFlags == None:
				new_Grid = Grid(gridNo, xi, yi)#, map_Coords  # a blank (green slate) for beginning use in map editor
			else:
				gridColour = map_green
				for i in mapFlags:
					index = mapFlags.index(i)
					# print "xi: %s, yi: %s, i: %s, index: %s" % (xi, yi, i, index)
					if i == (xi, yi):  # could have used "if (xi, yi) in mapflags:" but there is more we need to do with this loop
						# print xi, yi, " in mapFlags"
						gridColour = map_yellow
					elif (index < len(mapFlags)-1):  # otherwise, we're at the end of the path (and incrementing 1 more index of mapFlags would be out of range)
						#print "index %s != map length %s" % (index, len(mapFlags)-1)
						if xi == i[0] and (yi > 0 and yi < 18):  # to avoid index out of range errors
							if (yi > i[1] and yi < mapFlags[index+1][1]) or (yi < i[1] and yi > mapFlags[index+1][1]): #a decision i made that all loops should only and always look forward (to avoid needless double-checking)
								gridColour = map_yellow
						if yi == i[1] and (xi > 0 and xi < 22):
							if (xi > i[0] and xi < mapFlags[index+1][0]) or (xi < i[0] and xi > mapFlags[index+1][0]):
								gridColour = map_yellow
				#elif: #if it's along the path to the next flag
				new_Grid = Grid(gridNo, xi, yi, gridColour) #map_Coords,
			grid_List.append(new_Grid)
			gridNo = gridNo + 1

def pathTesting(returnStartPoint = False):  # loops through grid_List and colours each one based on if the checkNeighbours method returns true
	pathFailure = False
	for i in grid_List:
		if i.colour in (map_yellow, red) and checkNeighbours(i) == "starting point":
			startPoint = i
		else:
			if i.colour in (map_yellow, red) and not checkNeighbours(i):
				i.colour = red
				pathFailure = True
				# print "ERROR: path not connected at point ", i.xi + 1, ", ", i.yi +1
			elif i.colour in (map_yellow, red) and checkNeighbours(i):
				i.colour = map_yellow
		i.render()
	if returnStartPoint and not pathFailure:
		return startPoint
	if pathFailure:
		return False
	else:
		return True  # doesnt really need to be in an else condition

def checkNeighbours(i):  # calculates the number of connections for just one grid (called to len(grid_List) number of times)
	connections = 0

	if i.yi != 0:  # prevents 'list index out of range' error - should replace with a try/catch
		if grid_List[i.number-22].colour in (map_yellow, red, path_blue):
			connections = connections + 1
	if i.yi != 17: # "", also, this is hardcoded and thus wouldnt allow for mapsize change
		if grid_List[i.number+22].colour in (map_yellow, red, path_blue):
			connections = connections + 1
	if i.xi != 0:
		if grid_List[i.number-1].colour in (map_yellow, red, path_blue):
			connections = connections + 1
	if i.xi != 21:
		if grid_List[i.number+1].colour in (map_yellow, red, path_blue):
			connections = connections + 1

	if connections < 2:
		if i.xi == 21  and connections == 1:
			return "starting point"
		elif i.xi == 0 and connections == 1:
			return "ending point"
		else:
			return False
	else:
		return True  # doesnt really need to be in an else condition

def colourSelect(colour, x, y, size, previousColour):
	global button_State
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	pygame.draw.rect(surface, colour, (x, y, size, size))
	#rect.center = (x, y)

	#if x + (size/2) > mouse[0] > x - (size/2) and y + (size/2) > mouse[1] > y - (size/2):  # if centered
	if x <= mouse[0] <= x + size and y <= mouse[1] <= y + size:
		#highlighted
		if click[0] == 1:
			#pressed
			button_State = 1
		if button_State == 1 and click[0] == 0:
			button_State = 0
			return colour
	return previousColour

def colourPainter(colour):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if click[0] == 1 and (map_Coords[0] <= mouse[0] <= (map_Coords[0] + map_Size[0])) and (map_Coords[1] <= mouse[1] <= (map_Coords[1] + map_Size[1])):
		for i in grid_List:
			if i.x <= mouse[0] < i.x + i.size and i.y <= mouse[1] < i.y + i.size:
				i.colour = colour
				#print "grid changed: ", i

def testMap():
	global testMapSuccessful
	global tempMapFlagCoords
	pathComplete = False

	#startPoint = (None, None)  # a tuple
	# mapRoute = []
	# tempMapFlagCoords = [(None, None)]  # a list (of tuples)

	if pathTesting():
		curGrid = pathTesting(True)
		print "curGrid: ", curGrid.xi, curGrid.yi

		startPoint = [(curGrid.xi + 1, curGrid.yi)]
		print "startPoint: ", startPoint
		for j in startPoint:  # encountered a weird bug, only seems to append if startPoint is an iterable
			tempMapFlagCoords.append(j)
		backDirection = "East"
	else:
		print "ERROR: Path not fully connected"
		return False

	loop = 0
	while not pathComplete:
		#direction = validDirectionSearch(backDirection, curGrid)
		print "loopNo:", loop
		routesFound = 0
		print "curgrid: ", curGrid.xi, curGrid.yi, ":"
		for i in otherDirections(backDirection):  #assured because we cannot move back on ourselves (no dead ends accepted)
			print i
			if i == "North" and curGrid.yi != 0:  # prevents 'list index out of range' error - should replace with a try/catch
				if grid_List[curGrid.number-22].colour == map_yellow:  # must have two seperate if statements to avoid index range error
					routesFound = routesFound + 1
					print "we're going %s" % (i)
					futureGrid = grid_List[curGrid.number-22]
					headingDirection = i
			if i == "East" and curGrid.xi != 21:
				if grid_List[curGrid.number+1].colour == map_yellow:
					routesFound = routesFound + 1
					print "we're going %s" % (i)
					futureGrid = grid_List[curGrid.number+1]
					headingDirection = i
			if i == "South" and curGrid.yi != 17:
				if grid_List[curGrid.number+22].colour == map_yellow:
					routesFound = routesFound + 1
					print "we're going %s" % (i)
					futureGrid = grid_List[curGrid.number+22]
					headingDirection = i
			if i == "West" and curGrid.xi != 0:
				if grid_List[curGrid.number-1].colour == map_yellow:
					routesFound = routesFound + 1
					print "we're going %s" % (i)
					futureGrid = grid_List[curGrid.number-1]
					headingDirection = i

		if headingDirection != otherDirections(backDirection)[1] or checkNeighbours(curGrid) == "ending point":  # if a right angle is taken
			backDirection = otherDirections(headingDirection)[1]

			flagPoint = [(curGrid.xi, curGrid.yi)]
			for j in flagPoint:
				tempMapFlagCoords.append(j)
			print "flagCoord DETECTED! at", flagPoint
			print "headingDirection: ", headingDirection, " - backDirection: ", backDirection

			if checkNeighbours(curGrid) == "ending point":
				pathComplete = True
				print "Path Complete"
				print tempMapFlagCoords
				testMapSuccessful = True
				return True
		if routesFound > 1:
			print "multiple routes found... HELP!"
			pathComplete = True
			return False

		curGrid.colour = path_blue
		curGrid.render()
		surface.blit(grid_OverlayImg, map_Coords)

		# limits surface update rate to a maximum of 60 frames per second
		clock.tick(fps)  # do i want to limit this?
		# Pygame function to update surface with what has been blit-ed
		pygame.display.flip()

		curGrid = futureGrid

		loop = loop + 1

		#raw_input("Press Enter to continue...")  #debug, no longer required

def otherDirections(direction):
	# if you only intend to recieve the opposite direction, opDir == otherDirections(direction)[2]
	if direction == "North":
		return "East", "South", "West"
	if direction == "East":
		return "South", "West", "North"
	if direction == "South":
		return "West", "North", "East"
	if direction == "West":
		return "North", "East", "South"

def saveMap():
	global tempMapFlagCoords

	textFile = open("MapFlagCoords.txt", 'r+')
	loop = True

	while loop:
		also = "T"
		savedMapName = raw_input("Type in the name of this map: ")
		if len(savedMapName) < 15:
			if len(savedMapName) <= 0:
				print "Sorry, that name is too short, please try again.\n"
			loop = False
		else:
			print "Sorry, that name was too long, please try again.\n"
			also = "Also, t"
		for line in textFile:
			if savedMapName in line:
				print "%shis map name already exists!" % (also)
				userResponce = raw_input("Would you like to overwrite '%s'? (Y/N)") % (savedMapName)
				if ('y' or 'Y' or 'yes' or 'Yes') in userResponce:
					print "Ok, overwriting..."
					loop = False

	print savedMapName
	writeline = ("%s=%s\n") % (savedMapName, tempMapFlagCoords)
	textFile.write(writeline)
	print "Map '%s' successfully saved!" % (savedMapName)

	tempMapFlagCoords = []
	textFile.close()

def getFlagCoords():  # again, only if input argument is blank (for now)
	mapFlags = []
	textFile = open('MapFlagCoords.txt', 'r')

	for line in textFile:
		if mapSelection in line:
			print "Yep, it's here: ", line

			line = line.split('=[')[1].split(']')[0]
			#  print "Split line: ", line

			tupleCount = line.count("(")
			print "number of tuples: ", tupleCount

			line = line.replace('(', ' ').replace('), (', ' ').replace(', ', ' ').replace(')', ' ').split()
			#  print "circumsised 'list' line: ", line

			for i in range(tupleCount):
				#  print "i%s type: %s" % (i, type(line[i]))
				mapFlags.append(((int(line[i])),(int(line[i+1]))))#
				for j in range(1):
					line.pop(0)

			# print "text mapFlags = ", mapFlags
			break
		print "No flagCoords could be found under the map name '%s'." % (mapSelection)

	textFile.close()

	generateGridList(mapFlags)
	print "done generateGridList! ^^^"

	# flagCoords = []
	for mx, my in mapFlags:
		flagCoords.append(((((mx) * 80 / 2.2) + map_Coords[0]), (((my) * 80 / 2.2) + map_Coords[1])))  # note: this may be problematic if x or y = 1?
	#  print flagCoords, type(flagCoords), type(flagCoords[0])
	return flagCoords

def getWaveInfo(waveNo):
	spawnList = []
	# reading in Wave Setup.txt
	waveFile = open("Wave Setup.txt", 'r')
	for line in waveFile:
		if ("%s) " % (waveNo)) in line:
			spawnRate = int(line.split('{')[1].split('}')[0])
			print "spawnRate = ", spawnRate

			creepCount = line.count(', ') + 1
			print "creepCount = ", creepCount

			#line = line.split(']')[0]
			line = line.split('[')[1].replace(', ',' ').split(']')[0].split()

			print "line = ", line
			print "spawnList =", spawnList
			for i in range(creepCount):
				print i
				print "--", line[i]
				spawnList.append(int(line[i]))
			break

	print "spawnList = ", spawnList
	waveFile.close()
	return spawnRate, creepCount, spawnList

# creep constructor function ...
def addCreep(creepVariant = None):
	from Creep import Creep
	global map_Entrance
	global creep_List

	if creepVariant != None:
		if map_Entrance != []:
			new_Creep = Creep(map_Entrance[0], (map_Entrance[1] - 15), creepVariant)  # - 15 so top left corner of pre-entrance tile
			print new_Creep
		else:
			new_Creep = Creep((map_Size[0] + map_Coords[0]), (((map_Size[1] + map_Coords[1]) / 2) + 12), creepVariant)  # temporary - depends on map type
	else:
		if map_Entrance != []:
			new_Creep = Creep(map_Entrance[0], (map_Entrance[1] - 15))
		else:
			new_Creep = Creep((map_Size[0] + map_Coords[0]), (((map_Size[1] + map_Coords[1]) / 2) + 12))
	creep_List.append(new_Creep)
	print "creep_List[0].x:", creep_List[0].x

def creepHealthCheck(creep):
	global death_List, playerBudget

	if creep.health == 0:
		print creep, "Died"
		# increment current path death count in death_List
		playerBudget = playerBudget + creep.cost
		print "playerBudget: ", playerBudget
		for i in death_List:
			if i[0] == creep.flagNo:
				i[1] = i[1] + 1
		print "death_List = ", death_List
		creepIndex = creep_List.index(creep)
		creep_List.pop(creepIndex)
		return True
	else:
		return False

# ------creep class goes here -------

# Tower constructor function ...
def placeTower():
	from Tower import Tower
	new_Tower = Tower(mouse[0], mouse[1], True)
	tower_List.append(new_Tower)

	print "creep_List:", creep_List
	print "tower_List:", tower_List

# ------tower class goes here ------


# ------grid class goes here ------



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
