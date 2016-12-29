import pygame, math, random, sys

# Global variables for now:
canvas_width = 1000
canvas_height = 800

map_Coords = (20, 140)

def main():
	pygame.init()

	# rendering 'canvas':

	canvas_dimensions = (canvas_width, canvas_height)
	surface = pygame.display.set_mode(canvas_dimensions)
	#map_Coords = (20, 140) # will eventually become global variable, but for now in drawMap function

	pygame.display.set_caption("Will's 100% awesome TD Game!!!")


	background = pygame.Surface(surface.get_size()) #creates "background" the same size as "surface"
	background = background.convert() # investigate?
	#background.fill((
	surface.fill((255, 255, 255))  # RGB (so white)

	# loading temp map background (probs move into '__init__(self)' method once needed:
	flagCoords = drawMap(canvas_height, canvas_width, surface)

	# spawning chekcpoint flags on mapFlags
	flagLocation = "/home/will/Desktop/Final_Year_Project/Graphics/checkpointFlag.jpg"
	checkpointFlag_Img = pygame.image.load(flagLocation)
	#checkpointFlag_Img = pygame.transform.scale(checkpointFlag_Img, (flag_width, flag_height))
	for i in flagCoords:
		mapFlag_CoordX = flagCoords[i][0]
		mapFlag_CoordY = flagCoords[i][1]
		surface.blit(checkpointFlag_Img, (mapFlag_CoordX, mapFlag_CoordY))

	# spawning creep sprite
	drawCreep(canvas_height, canvas_width, surface)

#	box = pygame.Rect((box_XCoord, box_YCoord), box_size) # '0, 0' means top-left corner of screen. '50, 50' means draw the square 50x50 pixels tall/wide.
#	pygame.draw.rect(surface, (0, 0, 255), box) # draw onto "surface", the colour "blue", this "box".

	while (True): #debug: creates an infinite loop, so window doesnt immediately close!
		pass
		#for event in pygame.event.get():
		#	if event.type == QUIT:
		#		pygame.quit ()
		#		sys.exit (0)
		pygame.display.flip() # "Ok Pygame, now do your thang" - basically the same as pygame.display.update()

def drawMap(canvas_height, canvas_width, surface):
	mapLocation = "/home/parallels/will/Final_Year_Project/Graphics/Background/Template(22x18).jpg"
	temp_MapImg = pygame.image.load(mapLocation) # OG size = '1760 x 1440'

	temp_MapImg = pygame.transform.scale(temp_MapImg, (int(canvas_width * 0.8), int(canvas_height * 0.8)))

	# should probs implement a 'try:, except: ' for each image render
	surface.blit(temp_MapImg, map_Coords)

	# "IF mapname = temp_MapIMG: " for example
	# in later implementations consider json.load(file) to load creep flag coords from txt file
	mapFlags = [(15, 8), (15, 3), (6, 3), (6, 10), (13, 10), (13, 16), (5, 16)] # creates a list of tuples (cant be altered later) - this is only a temp variable

	flagCoords = []
	for mx, my in mapFlags:
	    flagCoords.append(((mx * 80) + map_Coords[0], (my * 80) + map_Coords[1]))

	print flagCoords
	return flagCoords

def drawCreep(canvas_height, canvas_width, surface): #Only a temporary method to clean up code while working on it
	creep_XCoord = canvas_width/2 #actually only want canvas_width
	creep_YCoord = canvas_height/2
	creep_size = (50, 50)
	creep_Img = pygame.image.load("/home/parallels/Desktop/Final_Year_Project/Graphics/Sprites/Creeps/Creep01_W.png")
	creep_Img = pygame.transform.scale(creep_Img, (creep_size[0], creep_size[1]))
	surface.blit(creep_Img, (creep_XCoord, creep_YCoord))

if __name__ == "__main__": #https://goo.gl/1CRvRx & https://goo.gl/xF4xOF
	main()

"""
# http://www.pygame.org/docs/ref/image.html#comment_pygame_image_load
class Sprite:
	def __init__(self):
		self.img = None
		self.pos = [0, 0]
		self.colourkey = [0, 0, 0] #most likely wont be used (maybe damage indication?)
		self.alpha = 255 #again, probs never used
"""
