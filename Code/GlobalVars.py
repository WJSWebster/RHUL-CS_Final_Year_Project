import pygame
pygame.init()

# Assigns the width and height of the screen as a tuple
canvas_width = 1000
canvas_height = 800
canvas_dimensions = (canvas_width, canvas_height)
surface = pygame.display.set_mode(canvas_dimensions)  # , FULLSCREEN

icon_Img = pygame.image.load(
    "Graphics/Sprites/Towers/Tower01_East.png").convert_alpha()
pygame.display.set_icon(icon_Img)

pygame.mouse.set_cursor(*pygame.cursors.arrow)

# Assigns the dimensions and the top-left coordinates of the map
map_Size = ((1760 / 2.2), (1440 / 2.2))
map_Coords = (20, 140)

# Manages how frequently surface updates ('flips')
clock = pygame.time.Clock()
fps = 60

# A list of all grid, creep, tower and rocket objects, respectively
grid_List = []
creep_List = []
tower_List = []
rocket_List = []
# A list to record the location and number of creep deaths during a game
death_List = []

# Represents what (single) object is 'highlighted' or selected by the player
entitySelected = None

# An integer of either 0 or 1, representing whether a menu button has been
# 'pressed' or not (such that action is only taken once button is
# 'un-pressed')
button_State = 0

# Default integers for the player's 'health' and 'budget' values and wave
# number the player is currently on for that map (re-assigned if save-data
# loaded)
playerHealth = 20
playerBudget = 20
waveNo = 1

# Tower variables:
# this is the ...
towerPlacement_Sound = pygame.mixer.Sound(
    "Sounds/Sound_Effects/TowerPlacement1.wav")
explosion_Sound = pygame.mixer.Sound("Sounds/Sound_Effects/ExplosionBang.wav")
firingRocket_Sound = pygame.mixer.Sound(
    "Sounds/Sound_Effects/RocketFiring.wav")
