import pygame
pygame.init()


# Assigns the width and height of the screen as a tuple
canvas_width = 1000
canvas_height = 800
canvas_dimensions = (canvas_width, canvas_height)
surface = pygame.display.set_mode(canvas_dimensions)  # , FULLSCREEN

icon_Img = pygame.image.load(
    "Graphics/Sprites/Towers/Rocketeer_East.png").convert_alpha()
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

gamePaused = False

# Font styles for titles and regular text used when render/'displaying'
# text on screen
largeText = pygame.font.SysFont('ubuntu', 80)  # 'ubuntu'
mediumText = pygame.font.SysFont('ubuntu', 50)
smallText = pygame.font.SysFont('ubuntu', 20)  # 'ubuntu'

# 3 element tuples (representing RGB values respectively) of commonly used
# colours in the program
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

# Mixer Variables:
soundEffectsVolume = 1.0
musicVolume = 1.0

# Sound Effects:..
towerPlacement_Sound = pygame.mixer.Sound(
    "Sounds/Sound_Effects/TowerPlacement1.wav")
firingCannon_Sound = pygame.mixer.Sound(
    "Sounds/Sound_Effects/CannonFiring.wav")
explosion_Sound = pygame.mixer.Sound("Sounds/Sound_Effects/ExplosionBang.wav")
firingRocket_Sound = pygame.mixer.Sound(
    "Sounds/Sound_Effects/RocketFiring.wav")
firingLaser_Sound = pygame.mixer.Sound("Sounds/Sound_Effects/LaserFiring.wav")
generatorPulsing_Sound = pygame.mixer.Sound(
    "Sounds/Sound_Effects/generatorPulsing.wav")

soundEffects_List = [towerPlacement_Sound, firingCannon_Sound, explosion_Sound,
                     firingRocket_Sound, firingLaser_Sound, generatorPulsing_Sound]

"""
# cannot assign music object to a variable
mapEditor_Music = pygame.mixer.music.load("Sounds/Music/First_In_Line.mp3")

print mapEditor_Music
music_List = [mapEditor_Music]
"""
