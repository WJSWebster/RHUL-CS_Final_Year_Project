import pygame

# Assigns the width and height of the screen as a tuple
canvas_width = 1000
canvas_height = 800
canvas_dimensions = (canvas_width, canvas_height)
surface = pygame.display.set_mode(canvas_dimensions)

# Assigns the dimensions and the top-left coordinates of the map
map_Size = ((1760 / 2.2), (1440 / 2.2))
map_Coords = (20, 140)

# A list of all grid, creep and tower objects, respectively
grid_List = []
creep_List = []
tower_List = []

# Represents what (single) object is 'highlighted' or selected by the player
entitySelected = None
