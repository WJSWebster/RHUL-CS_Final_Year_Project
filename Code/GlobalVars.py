import pygame
pygame.init()

# Assigns the width and height of the screen as a tuple
canvas_width = 1000
canvas_height = 800
canvas_dimensions = (canvas_width, canvas_height)
surface = pygame.display.set_mode(canvas_dimensions) #, FULLSCREEN

# Assigns the dimensions and the top-left coordinates of the map
map_Size = ((1760 / 2.2), (1440 / 2.2))
map_Coords = (20, 140)

# A list of all grid, creep, tower and rocket objects, respectively
grid_List = []
creep_List = []
tower_List = []
rocket_List = []
# A list to record the location and number of creep deaths during a game
death_List = []

# Represents what (single) object is 'highlighted' or selected by the player
entitySelected = None

# Tower variables:
# this is the ...
towerPlacement_Sound = pygame.mixer.Sound("Sounds/Sound_Effects/TowerPlacement1.wav")
explosion_Sound = pygame.mixer.Sound("Sounds/Sound_Effects/ExplosionBang.wav")
firingRocket_Sound = pygame.mixer.Sound("Sounds/Sound_Effects/RocketFiring.wav")
