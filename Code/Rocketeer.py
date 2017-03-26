from main import surface, entitySelected, creep_List, firingRocket_Sound, rocket_List
from Tower import *
import pygame
import math

pygame.init()


class Rocketeer(Tower):  # need to make derived from turret class
    def __init__(self, x, y, hover):  # maybe not needed, as seen above ^^
        #from main import creep_List
        #super(Rocketeer, self).__init__()
        Tower.__init__(self, x, y, hover)

        self.typeNo = 2
        self.type, self.damage, self.cooldownTime, self.radius, self.cost = Tower.getType(
            self)
        #self.x, self.y = x, y

        #self.size = 28
        #self.direction = None
        # self.hover = hover  # most likely True?

        #self.attacking = False
        #self.attackFrameCount = 0
        #self.target = None
        
    """
    def getType(self):  # duplicate method to tower, either change parameters or derive from tower class
        typeFile = open("Types.txt", 'r')

        parsing = False

        for line in typeFile:
            if"[%s]" % (self.typeNo) in line:
                typeName = line.split("] ")[1].split(":")[0]
                parsing = True
            elif parsing and "Damage =" in line:
                damage = line.split(" = ")[1]
            elif parsing and "Attack Speed =" in line:
                cooldownTime = line.split(" = ")[1]
            elif parsing and "Radius =" in line:
                radius = line.split(" = ")[1]
            elif parsing and "Cost =" in line:
                cost = line.split(" = ")[1]
            elif "[%s]" % (self.typeNo + 1) in line:
                parsing = False
                break

        typeFile.close()
        return (typeName, int(damage), int(cooldownTime), int(radius), int(cost))
    """

    def targetFinder(self):  # duplicate method, should be removed when is derived class of Tower
        self.radius = 20  # assign in __init__
        range_List = []
        for i in creep_List:
            # if (i.x within sprite.rect +-self.range) and (i.y within
            # sprite.rect +-self.range):
            range_List.append(i)
        # for i in range_List:
            # self.target = the one with the highest flagNo & closest to next

        if len(creep_List) != 0:
            self.target = creep_List[0]
            return True
        else:
            print self, "no creeps in creep_List"
            return False

    def rocketAttack(self):  # could also be joined to attack method once class is derived
        from Rocket import Rocket

        if not self.attacking:
            if self.targetFinder():
                self.rotate()
                if self.direction != None:
                    pygame.mixer.Sound.play(firingRocket_Sound)
                    newRocket = Rocket(self, self.target,
                                       self.direction, self.damage)
                    rocket_List.append(newRocket)

                    self.attacking = True
                    self.attackFrameCount = 1
        else:
            if self.attackFrameCount == self.cooldownTime:
                self.attacking = False
                self.target = None
                self.direction = None
            self.attackFrameCount = self.attackFrameCount + 1

    def rotate(self):
        import math  # this is the second example of this import, TODO tidy up

        selfPos = (self.x, self.y)
        targetPos = (self.target.x, self.target.y)

        angleVector = self.getAngle(selfPos, targetPos)

        print "angleVector: ", angleVector

        if 315 <= angleVector < 361 or 0 <= angleVector < 45:
            direction = "North"
        elif 45 <= angleVector < 135:
            direction = "East"
        elif 135 <= angleVector < 225:
            direction = "South"
        elif 225 <= angleVector < 315:
            direction = "West"
        else:
            print "ERROR: angle not within any valid direction range (%s)" % (str(angleVector))
            return None

        print "Direction: ", direction

        self.direction = direction
        return angleVector

    # only takes in these arguments when rendering again in stats screen
    def render(self, xCoord=None, yCoord=None):
        if self.hover:  # not yet placed
            # need to replace with it's own Sprite
            self.image = pygame.image.load(
                "Graphics/Sprites/Towers/Tower01_Transparent.png").convert_alpha()
            pygame.mouse.set_visible(False)
        else:
            if xCoord == None and yCoord == None:  # means that turret doesnt double it's firing speed
                self.rocketAttack()  # really, this whole method should be an 'update()' method instead as it's doing way more than just rendering - same for all classes

            if self.target != None and self.direction != None:  # placed and has target
                self.image = pygame.image.load(
                    "Graphics/Sprites/Towers/Tower01_%s.png" % (self.direction)).convert_alpha()
            else:  # placed but no tower
                self.image = pygame.image.load(
                    "Graphics/Sprites/Towers/Tower01.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        if xCoord == None and yCoord == None:
            surface.blit(self.image, (self.x, self.y))

            if entitySelected == self:
                silhouette_Img = pygame.image.load(
                    "Graphics/Sprites/Towers/TowerSilhouette.png").convert_alpha()
                silhouette_Img = pygame.transform.scale(
                    silhouette_Img, (self.size, self.size))
                surface.blit(silhouette_Img, (self.x, self.y))

            if not self.hover:
                self.rocketAttack()
        else:
            surface.blit(self.image, (xCoord, yCoord))
