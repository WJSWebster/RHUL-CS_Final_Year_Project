# from GlobalVars import playerHealth, entitySelected, smallText, red  # , surface, # this is necessay
# from main import creepHealthCheck, displayText  # refers to methods in
# main, and as such are required imports from main

from GlobalVars import playerHealth, entitySelected, smallText, red  # , surface,
from main import creepHealthCheck, displayText

import pygame
pygame.init()


class Creep(pygame.sprite.Sprite):
    def __init__(self, x, y, speciesNo=1):
        # calls to the __init__ constructor in the 'Sprite' parent class
        super(Creep, self).__init__()
        # pygame.sprite.Sprite.__init__(self)

        self.x = int(x)
        self.y = int(y)

        self.size = 28
        self.direction = 'West'

        self.flagNo = 0
        self.pathComplete = False

        self.species, self.health, self.damage, self.speed, self.cost = self.getSpecies(
            speciesNo)

        self.image = pygame.image.load(
            "Graphics/Sprites/Creeps/%s_West.png" % (self.species)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.radius = self.size - 10

        # only for attackedText function
        self.attackedFrameCount = None
        self.attackedXCoord = None
        self.attackedYCoord = None
        self.attackedDamageAmount = None

    def getSpecies(self, speciesNo):
        speciesFile = open("Species.txt", 'r')

        parsing = False

        for line in speciesFile:
            if "[%s]" % (speciesNo) in line:
                species = line.split("] ")[1].split(":")[0]
                parsing = True
            elif parsing and "Health =" in line:
                health = line.split(" = ")[1]
            elif parsing and "Damage" in line:
                damage = line.split(" = ")[1]
            elif parsing and "Speed" in line:
                speed = line.split(" = ")[1].split("\n")[0]
            elif parsing and "Cost" in line:
                cost = line.split(" = ")[1]
                parsing = False
            elif "[%s]" % (speciesNo + 1) in line:
                parsing = False
                break

        speciesFile.close()
        if float(speed) < 1:
            return (species, int(health), int(damage), float(speed), int(cost))
        else:
            return (species, int(health), int(damage), int(speed), int(cost))

    def creepPathFollow(self, flagCoords):
        if self.flagNo == len(flagCoords):
            print self, ": Complete"
            self.pathComplete = True
        else:  # TODO maybe need to use int() to round values? (as being a float maybe confusing when trying to divide into fractions of a pixel)
            if (flagCoords[self.flagNo][0] + (self.speed / 2)) > self.x > (flagCoords[self.flagNo][0] - (self.speed / 2)) and (flagCoords[self.flagNo][1] + (self.speed / 2)) > self.y > (flagCoords[self.flagNo][1] - (self.speed / 2)):
                self.flagNo += 1
                # print self, " flagNo = ", self.flagNo  #debug
            else:
                if not (flagCoords[self.flagNo][0] + (self.speed / 2)) > self.x > (flagCoords[self.flagNo][0] - (self.speed / 2)):
                    if self.x < flagCoords[self.flagNo][0]:
                        self.direction = 'East'
                        self.x += self.speed
                        # print self.x, " < ", flagCoords[flagNo][0]
                    elif self.x > flagCoords[self.flagNo][0]:
                        self.direction = 'West'
                        self.x -= self.speed
                        # print self.x, " > ", flagCoords[flagNo][0]
                elif not (flagCoords[self.flagNo][1] + (self.speed / 2)) > self.y > (flagCoords[self.flagNo][1] - (self.speed / 2)):
                    if self.y < flagCoords[self.flagNo][1] + (self.speed / 2):
                        self.direction = 'South'
                        self.y += self.speed
                    elif self.y > flagCoords[self.flagNo][1]:
                        self.direction = 'North'
                        self.y -= self.speed
            # print "x = ", self.x, ", y = ", self.y

    def attacked(self, damage):
        self.health = self.health - damage
        self.attackedText(damage)
        creepHealthCheck(self)

    # make class so multiple damageText objects can exist at once
    def attackedText(self, damageAmount=None):
        if damageAmount != None:  # attackedText just initialised
            self.attackedFrameCount = 0
            self.attackedXCoord = self.x
            self.attackedYCoord = self.y
            self.attackedDamageAmount = damageAmount
        else:
            if self.attackedFrameCount != None:
                if self.attackedFrameCount <= 35:
                    displayText("-%s" % (self.attackedDamageAmount), smallText, red,
                                self.attackedXCoord, (self.attackedYCoord - self.attackedFrameCount))
                    # TODO figure out a way of making this go transparent over
                    # course of framCount (?)
                    self.attackedFrameCount = self.attackedFrameCount + 1
                else:
                    self.attackedFrameCount = None
                    self.attackedXCoord = None
                    self.attackedYCoord = None
                    self.attackedDamageAmount = None

    def attackPlayer(self):
        #from main import creep_List
        global playerHealth, creep_List

        print "creep attacking!"

        playerHealth = playerHealth - self.damage

        creepIndex = creep_List.index(self)
        creep_List.pop(creepIndex)

    def render(self, xCoord=None, yCoord=None):
        from main import surface
        #global surface

        #############################
        """
        # only used in debug as part of laser CollisionTest.py
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if window close button pressed
                pygame_quit()
        mouse = pygame.mouse.get_pos()
        self.x = mouse[0]
        self.y = mouse[1]
        self.direction = "West"
        """
        #############################

        # http://programarcadegames.com/python_examples/f.php?file=sprite_collect_graphic.py
        self.image = pygame.image.load(
            "Graphics/Sprites/Creeps/%s_%s.png" % (self.species, self.direction)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)

        if xCoord == None and yCoord == None:  # rendering on game map
            surface.blit(self.image, (self.x, self.y))

            if entitySelected == self:
                silhouette_Img = pygame.image.load(
                    "Graphics/Sprites/Creeps/CreepSilhouette_%s.png" % (self.direction)).convert_alpha()
                silhouette_Img = pygame.transform.scale(
                    silhouette_Img, (self.size, self.size))
                surface.blit(silhouette_Img, (self.x, self.y))
        else:  # rendering as part of stats panel
            surface.blit(self.image, (xCoord, yCoord))
        self.attackedText()
        #  pygame.draw.rect(surface, red, (self.x, self.y, self.width, self.height))
