from main import surface, entitySelected, creep_List
from Tower import *
import pygame

pygame.init()


class Laser(Tower):
    def __init__(self, x, y, hover):
        Tower.__init__(self, x, y, hover)

        self.typeNo = 3
        self.type, self.damage, self.cooldownTime, self.radius, self.cost = Tower.getType(
            self)
        # aka 4 seconds (@60FPS), or 8 damage to each creep in laser
        self. attackTime = 240

        self.hover_IMG = pygame.image.load(
            "Graphics/Sprites/Towers/Tower01_Transparent.png").convert_alpha()  # TODO replace with transparrent Tower03
        self.hover_IMG = pygame.transform.scale(
            self.hover_IMG, (self.size, self.size))
        self.originalImage = pygame.image.load(
            "Graphics/Sprites/Towers/Tower03.png").convert_alpha()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.size, self.size))


        self.direction = 0.0  # the angle the turret is facing
        self.rotAmount = 1.5  # the amount that the turret can rotate every frame

        # the angle vector between the turret and target positions (float)
        self.targetAngle = None

    def targetFinder(self):  # duplicate method, should be removed when is derived class of Tower
        """
        self.range = 20  # assign in __init__
        range_List = []
        for i in creep_List:
            # if (i.x within sprite.rect +-self.range) and (i.y within sprite.rect +-self.range):
                range_List.append(i)
        for i in range_List:
            # self.target = the one with the highest flagNo & closest to next
        """

        if len(creep_List) != 0:
            self.target = creep_List[0]
            print "target found!"
            self.getTargetAngle()
            return True
        else:
            print self, "no creeps in creep_List"
            return False

    def getTargetAngle(self):
        self.targetAngle = self.getAngle(
            (self.x, self.y), (self.target.x, self.target.y))

    def rotateToTarget(self):
        self.getTargetAngle()

        # if on target or already attacking return True
        if self.direction - 5 <= self.targetAngle <= self.direction + 5 or self.attacking: # doesnt move if firing
            self.image = pygame.transform.rotate(self.originalImage, -self.direction)
            return True

        elif self.direction < self.targetAngle:
            print "target clockwise"
            self.direction += self.rotAmount
        else:  # if self.direction > self.targetAngle
            print "target anti-clockwise"
            self.direction -= self.rotAmount
            print self.direction


        if self.direction >= 360:  # not strictly essential
            self.direction -= 360
        elif self.direction < 0:
            self.direction += 360

        self.image = pygame.transform.rotate(self.originalImage, -self.direction) # - amount = rotate clockwise

        print self.direction

        return False

    def laserAttack(self):  # should all be called attack method for easy instancing  # could also be joined to attack method once class is derived
        if not self.attacking:
            self.attacking = True
            self.attackFrameCount = 1
        else:

            """
            laser_Img = pygame.image.load("Graphics/Sprites/Towers/Lasers/Laser_%s.png" % (
                int(self.attackFrameCount / 24))).convert_alpha()  # TODO investigate
            laser_Img = pygame.transform.scale(laser_Img, (500, 50))
            """
            laser_Img = pygame.image.load("Graphics/Sprites/Towers/Lasers/Laser_TEST.png").convert_alpha()
            laser_Img = pygame.transform.scale(laser_Img, (1200, 20))
            laser_Img = pygame.transform.rotozoom(laser_Img, -self.direction + 90, 0.5)

            #laser_Rect = pygame.draw.rect(surface, red, (self.x, self.y, 500, 50))

            laserX = (self.x + (self.size / 2)) - (laser_Img.get_width() / 2)
            laserY = (self.y + (self.size / 2)) - (laser_Img.get_height() / 2)

            surface.blit(laser_Img, (laserX, laserY))

            if self.attackFrameCount == self.attackTime:
                self.attacking = False
                self.target = None
                self.targetAngle = None

                self.cooldownTimeFrameCount = 0
            self.attackFrameCount = self.attackFrameCount + 1

    # only takes in these arguments when rendering again in stats screen
    def render(self, xCoord=None, yCoord=None):
        if self.hover:  # not yet placed
            surface.blit(self.hover_IMG, (self.x, self.y))
            pygame.mouse.set_visible(False)
        else:
            if xCoord == None and yCoord == None:  # means that turret doesnt double it's firing speed
                # if turret has a target (avoids no attribut errors)
                if self.target != None:
                    if self.rotateToTarget() and self.cooldownTimeFrameCount >= self.cooldownTime:
                        self.laserAttack()  # really, this whole method should be an 'update()' method instead as it's doing way more than just rendering - same for all classes
                else:
                    # idol sprite image
                    self.image = self.originalImage
                    self.targetFinder()

                surface.blit(self.image, (self.x, self.y))

                if entitySelected == self:
                    silhouette_Img = pygame.image.load(
                        "Graphics/Sprites/Towers/TowerSilhouette.png").convert_alpha()  # TODO replace with turret03 silhouette image
                    silhouette_Img = pygame.transform.scale(
                        silhouette_Img, (self.size, self.size))
                    surface.blit(silhouette_Img, (self.x, self.y))
            else:  # rendering in stats screen
                surface.blit(self.image, (xCoord, yCoord))

            # keeps incrementing while attacking and reset to zero after attack
            # TODO seems inefficient
            self.cooldownTimeFrameCount += 1
