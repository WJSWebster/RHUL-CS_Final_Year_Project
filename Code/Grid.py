import random
import pygame
pygame.init()

from GlobalVars import map_Coords, surface  # , frameCounter


map_green = (70, 147, 65)
map_yellow = (220, 170, 20)
map_grey = (135, 135, 135)
path_blue = (0, 191, 255)

map_brown = (154, 108, 16)  # used for when path is tunn


class Grid:
    def __init__(self, number, xi, yi, colour=map_green):

        self.number = number

        self.xi = xi  # 0 - 21
        self.yi = yi  # 0 - 17

        self.size = 36.5

        self.x = (xi * self.size) + map_Coords[0]
        self.y = (yi * self.size) + map_Coords[1]

        #self.direction = direction
        self.colour = colour
        self.randColour = []

        divergenceAmount = 10

        for i in self.colour:
            if bool(random.getrandbits(1)):
                randDivergence = i + random.randint(0, divergenceAmount)
            else:
                randDivergence = i - random.randint(0, divergenceAmount)
            self.randColour.append(randDivergence)

        for i, c in enumerate(self.randColour):
            if c < 0:
                self.randColour[i] = 0
            elif c > 255:
                self.randColour[i] = 255

        # print "self.randColour: ", self.randColour

    def checkNeighbours():
        # TODO maybe want to do this in each loop of makeMap
        pass

    def render(self, rand=False):  # , x = self.x, y = self.y, colour = self.colour
        #from main import frameCounter
        # print self.colour, type(self.colour)
        # print self.randColour, type(self.randColour)
        """
        if frameCounter % 1 == 0:
            self.randColour = []

            divergenceAmount = 10

            for i in self.colour:
                if bool(random.getrandbits(1)):
                    randDivergence = i + random.randint(0, divergenceAmount)
                else:
                    randDivergence = i - random.randint(0, divergenceAmount)
                self.randColour.append(randDivergence)

            for i, c in enumerate(self.randColour):
                if c < 0:
                    self.randColour[i] = 0
                elif c > 255:
                    self.randColour[i] = 255

            #print self.randColour, type(self.randColour)
        """

        if rand:  # ie, in map editor, not in game
            pygame.draw.rect(surface, self.randColour,
                             (self.x, self.y, self.size, self.size))
        else:
            pygame.draw.rect(surface, self.colour,
                             (self.x, self.y, self.size, self.size))
