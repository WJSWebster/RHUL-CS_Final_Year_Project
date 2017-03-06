#from Creep import *  # cannot render because makes calls to 'surface'
#from Tower import *
#import __ini__
import pygame, math, random, sys

# Global variables for now:
canvas_width = 1000
canvas_height = 800

map_Size = ((1760 / 2.2), (1440 / 2.2))
map_Coords = (20, 140)

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
path_blue = (0,191,255)

button_State = 0

# already within resetGameState()!
playerHealth = 20
playerBudget = 0
creep_List = []
death_List = []
tower_List = []
entitySelected = None
mapSelection = ""
waveNo = 1
frameCounter = 1
# stars = "" # this is pulled from the player's save text file
flagCoords = []
map_Entrance = ()
grid_List = []
tempMapFlagCoords = []

testMapSuccessful = False

creep_Speed = 1  # temporary - later refer to "bible"

# setting 'canvas':
canvas_dimensions = (canvas_width, canvas_height)
surface = pygame.display.set_mode(canvas_dimensions)

# assigning menuBackground:
menuBackground = pygame.image.load("Graphics/Background/Main_Background.png")

#assigning grid_OverlayImg:
#grid_OverlayImg = pygame.image.load("Graphics/Background/Grid_Overlay(Test).png")
grid_OverlayImg = pygame.image.load("Graphics/Background/Grid_Overlay.png")
grid_OverlayImg = pygame.transform.scale(grid_OverlayImg, (int(map_Size[0]), int(map_Size[1])))

deltaTime = 0
getTicksLastTime = 0

def resetGameState():
	global playerHealth, creep_List, death_List, tower_List, mapSelection, waveNo, stars, flagCoords, map_Entrance, grid_List
	playerHealth = 20
	playerBudget = 0
	creep_List = []
	death_List = []
	tower_List = []
	mapSelection = ""
	waveNo = 1
	frameCounter = 1
	# stars = ""
	flagCoords = []
	map_Entrance = ()
	grid_List = []
	generateGridList()

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
			button = pygame.image.load("Graphics/Sprites/Buttons/%s_Highlighted.png" % (colour))
			if click[0] == 1:
				button = pygame.image.load("Graphics/Sprites/Buttons/%s_Pressed.png" % (colour))
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
			button = pygame.image.load("Graphics/Sprites/Buttons/%s.png" % (colour))
	else:
		button = pygame.image.load("Graphics/Sprites/Buttons/%s.png" % (colour))
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
		pygame.display.flip()  # "Ok Pygame, now do your thang" - basically the same as pygame.display.update()

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
		pygame.display.flip()

def main():
	global map_Entrance, death_List, waveNo, frameCounter
	pygame.display.set_caption("Will's TD Game -- Game")

	# rendering 'canvas':
	surface.fill(white)

	# rendering background image
	background_Img = pygame.image.load("Graphics/Background/Game_Background.png")

	"""
	# loading temp map background
	temp_MapImg = pygame.image.load("Graphics/Background/Template(22x18).jpg")  # OG size = '1760 x 1440'
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
	checkpointFlag_Img = pygame.image.load("Graphics/checkpointFlag.jpg")
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

			if waveNo != 1:  # error checking
				print "waveNo =", waveNo
				print "frameCounter =", frameCounter

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
			if event.type == pygame.QUIT:
				pygame_quit()
		pygame.display.flip()  # basically the same as pygame.display.update()

def checkSelected(mouse, click, curEntity):
	global button_State, entitySelected
	dataXCoord = canvas_width - 90
	dataYCoord = 175  # initially, then incremented upon on future lines of data
	statsBackground = pygame.image.load("Graphics/Sprites/Buttons/Grey.png")
	#statsBackground = pygame.image.load("Graphics/Sprites/Buttons/Orange_pressed.png")
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
	pygame.display.set_caption("Will's TD Game -- Map Editor")

	surface.fill(map_grey)
	"""
	# loading temp map background
	temp_MapImg = pygame.image.load("Graphics/Background/Template(22x18).jpg")  # OG size = '1760 x 1440'
	temp_MapImg = pygame.transform.scale(temp_MapImg, (int(map_Size[0]), int(map_Size[1])))
	"""

	"""
	index = 0
	for yi in range(18):
		for xi in range(22):
			new_Grid = Grid(index, xi, yi)
			grid_List.append(new_Grid)
			index = index + 1
	"""

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
			if event.type == pygame.QUIT:
				pygame_quit()
		pygame.display.flip()  # basically the same as pygame.display.update()

def generateGridList(mapFlags = None):
	global grid_List

	gridNo = 0

	print mapFlags

	for yi in range(18):
		for xi in range(22):
			if mapFlags == None:
				new_Grid = Grid(gridNo, xi, yi)  # a blank (green slate) for beginning use in map editor
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
				new_Grid = Grid(gridNo, xi, yi, gridColour)
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

def addCreep(creepVariant = None):
	global map_Entrance

	if creepVariant != None:
		pass # in future, search through text file and read in creep's statement
	if map_Entrance != []:
		new_Creep = Creep(map_Entrance[0], (map_Entrance[1] - 15))  # - 15 so top left corner of pre-entrance tile
	elif creepVariant != None:
		print "ERROR: no map_Entrance defined!"
		new_Creep = Creep((map_Size[0] + map_Coords[0]), (((map_Size[1] + map_Coords[1]) / 2) + 12))  # temporary - depends on map type
	else:
		new_Creep = Creep((map_Size[0] + map_Coords[0]), (((map_Size[1] + map_Coords[1]) / 2) + 12), creepVariant)
	creep_List.append(new_Creep)

def creepHealthCheck(creep):
	global death_List, playerBudget

	if creep.health == 0:
		print creep, "Died"
		# increment current path death count in death_List
		playerBudget = playerBudget + creep.cost
		for i in death_List:
			if i[0] == creep.flagNo:
				i[1] = i[1] + 1
		print "death_List = ", death_List
		creepIndex = creep_List.index(creep)
		creep_List.pop(creepIndex)
		return True
	else:
		return False


class Creep:
	def __init__(self, x, y, speciesNo = 1):
		self.x = int(x)
		self.y = int(y)

		self.size = 28
		self.direction = 'West'

		self.flagNo = 0
		self.pathComplete = False

		self.species, self.health, self.damage, self.speed, self.cost = self.getSpecies(speciesNo)
		#need to move 'creep_speed = 1' here

		#self.attackDamage = 2 # again, a default stat for now...

		#only for attackedText function
		self.attackedFrameCount = None
		self.attackedXCoord = None
		self.attackedYCoord = None
		self.attackedDamageAmount = None

	def getSpecies(self, speciesNo):
		speciesFile = open("Species.txt", 'r')

		parsing = False

		for line in speciesFile:
			if ("[%s]") % (speciesNo) in line:
				species = line.split("] ")[1].split(":")[0]
				parsing = True
			elif parsing and "Health =" in line:
				health = line.split(" = ")[1]
			elif parsing and "Damage" in line:
				damage = line.split(" = ")[1]
			elif parsing and "Speed" in line:
				speed = line.split(" = ")[1]
			elif parsing and "Cost" in line:
				cost = line.split(" = ")[1]
			elif "[" in line:
				parsing = False
				break

		speciesFile.close()
		return (species, int(health), int(damage), int(speed), int(cost))

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
		#print self, " health = ", self.health
		creepHealthCheck(self)
		self.attackedText(damage)

	def attackedText(self, damageAmount = None):
		if damageAmount != None:  # attackedText just initialised
			self.attackedFrameCount = 0
			self.attackedXCoord = self.x
			self.attackedYCoord = self.y
			self.attackedDamageAmount = damageAmount
		else:
			if self.attackedFrameCount != None:
				if self.attackedFrameCount <= 35:
					displayText("-%s" % (self.attackedDamageAmount), smallText, red, self.attackedXCoord, (self.attackedYCoord - self.attackedFrameCount))
					# figure out a way of making this go transparent over course of framCount (?)
					self.attackedFrameCount = self.attackedFrameCount + 1
				else:
					self.attackedFrameCount = None
					self.attackedXCoord = None
					self.attackedYCoord = None
					self.attackedDamageAmount = None

	def attackPlayer(self):
		global playerHealth

		playerHealth = playerHealth - self.damage

		creepIndex = creep_List.index(creep)
		creep_List.pop(creepIndex)

	def render(self, xCoord = None, yCoord = None): #, xRendCoord = self.x, yRendCoord = self.y
		creep_Img = pygame.image.load("Graphics/Sprites/Creeps/%s_%s.png" % (self.species, self.direction))
		creep_Img = pygame.transform.scale(creep_Img, (self.size, self.size))
		if xCoord == None and yCoord == None:
			surface.blit(creep_Img, (self.x, self.y))
		else:
			surface.blit(creep_Img, (xCoord, yCoord))
		self.attackedText()
		#  pygame.draw.rect(surface, red, (self.x, self.y, self.width, self.height))

def placeTower():
	new_Tower = Tower(mouse[0], mouse[1], True)
	tower_List.append(new_Tower)

class Tower:
	def __init__(self, x, y, hover):
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
		self.shadow_Img = pygame.image.load("Graphics/Sprites/Other/Shadow.png")
		self.cannonBall_Img = pygame.transform.scale(pygame.image.load("Graphics/Sprites/Other/CannonBall.png"), (self.size, self.size))
		self.explosion_Img = pygame.transform.scale(pygame.image.load("Graphics/Sprites/Other/Explosion.png"), (self.size, self.size))

		self.explosionSize = int(self.size * 2)
		self.aftermathFrameCount = 0
		self.aftermathXCoord = None
		self.aftermathYCoord = None
		self.aftermathBool = False


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
				self.attackFrameCount = 1  # re-assigned at the beginning (maybe?)
		else:
			if self.attackFrameCount == self.attackSpeed:  # attack frame
				self.target.attacked(self.damage)
				print "\n"
				print "targetXInitial: ", self.targetXInitial
				self.cannonBallAftermath(self.targetXInitial, self.targetYInitial)
				self.attacking = False
				self.target, self.targetXInitial, self.targetYInitial = None, None, None
			elif self.attackFrameCount < self.attackSpeed:  # attack coming
				sizeMultiplied = int(self.size + (self.size - ((float(self.attackFrameCount) / self.attackSpeed) * self.size)))
				fallDistance = float((self.attackSpeed - self.attackFrameCount) / 0.25)
				print "sizeMultiplied: ", sizeMultiplied

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
			explosion_Img = pygame.image.load("Graphics/Sprites/Explosions/Explosion_%s.png" % (int(self.aftermathFrameCount / 5)))
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
			tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01_Transparent.png")
			pygame.mouse.set_visible(False)
			#  pygame.mouse.set_cursor  # https://www.pygame.org/docs/ref/mouse.html#pygame.mouse.set_cursor
		else:
			#self.cannonBallAttack()
			if self.direction == "None":
				tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01.png")
			else:
				tower_Img = pygame.image.load("Graphics/Sprites/Towers/Tower01_%s.png" % (self.direction))

		tower_Img = pygame.transform.scale(tower_Img, (self.size, self.size))
		if xCoord == None and yCoord == None:
			surface.blit(tower_Img, (self.x, self.y))
			if not self.hover:
				self.cannonBallAttack()
		else:
			surface.blit(tower_Img, (xCoord, yCoord))
			if self.aftermathBool:
				self.cannonBallAftermath()


class Grid:
	def __init__ (self, number, xi, yi, colour = map_green, direction = None):
		self.number = number

		self.xi = xi  # 0 - 21
		self.yi = yi  # 0 - 17

		self.size = 36.5

		self.x = (xi * self.size) + map_Coords[0]
		self.y = (yi * self.size) + map_Coords[1]

		#self.direction = direction

		self.colour = colour

	def checkNeighbours():
		# maybe want to do this in each loop of makeMap
		pass

	def render(self): #, x = self.x, y = self.y, colour = self.colour
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
