import pygame, math, random, sys


def main():
	pygame.init()

	# rendering 'canvas':
	canvas_width = 1000
	canvas_height = 800
	surface = pygame.display.set_mode((canvas_width, canvas_height))

	pygame.display.set_caption("Will's 100% awesome TD Game!!!")

	
	background = pygame.Surface(surface.get_size()) #creates "background" the same size as "surface"
	background = background.convert() # investigate?
	#background.fill((
	surface.fill((0, 0, 255))  # RGB (so white)

	# loading temp map background (probs move into '__init__(self)' method once needed:
	temp_MapImg = pygame.image.load("/home/parallels/Desktop/Final_Year_Project/Graphics/Background/Template(22x18).jpg")
	pygame.transform.scale(temp_MapImg, (1280, 720))
	# should probs implement a 'try:, except: ' for each image render
	surface.blit(temp_MapImg, (0, 0))
	

	"""
	box_XCoord = 0 
	box_YCoord = 0 # the x & y coordinates of the box
	box_size = (50, 50)
	box = pygame.Rect((box_XCoord, box_YCoord), box_size) # '0, 0' means top-left corner of screen. '50, 50' means draw the square 50x50 pixels tall/wide.
	pygame.draw.rect(surface, (0, 0, 255), box) # draw onto "surface", the colour "blue", this "box".
	"""

	pygame.display.flip() # "Ok Pygame, now do your thang"

	while (True): # debug: creates an infinite loop, so window doesnt immediately close!
		pass

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
