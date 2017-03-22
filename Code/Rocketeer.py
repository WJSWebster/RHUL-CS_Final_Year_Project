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
        self.type, self.damage, self.attackSpeed, self.cost = Tower.getType(
            self)
        self.x, self.y = x, y

        self.size = 28
        self.hover = hover  # most likely True?

        self.attacking = False
        self.attackFrameCount = 0
        self.target = None

        self.direction = None

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
                attackSpeed = line.split(" = ")[1]
            elif parsing and "Cost =" in line:
                cost = line.split(" = ")[1]
            elif "[%s]" % (self.typeNo + 1) in line:
                parsing = False
                break

        typeFile.close()
        return (typeName, int(damage), int(attackSpeed), int(cost))

    def targetFinder(self):  # duplicate method, should be removed when is derived class of Tower
        from main import creep_List

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
            if self.attackFrameCount == self.attackSpeed:
                self.attacking = False
                self.target = None
                self.direction = None
            self.attackFrameCount = self.attackFrameCount + 1

    def rotate(self):
        import math  # this is the second example of this import, need to tidy up

        """
        # Calculating distance between two points using pythagorus:
        diff = (self.target.x - self.x, self.target.y - self.y)  # https://docs.python.org/2/library/math.html#math.atan2
        pythagDiff = math.sqrt(diff[0]**2 + diff[1]**2)
        """

        targetPos = (self.target.x, self.target.y)
        selfPos = (self.x, self.y)

        """
        yDiff = (self.y, self.target.y)
        xDiff = (self.x, self.target.x)

        angleVector = self.angle_clockwise(xDiff, yDiff)
        #angleVector = math.degrees(math.atan(yOpp/xAdj))
        """

        # http://stackoverflow.com/a/23408996
        angleVector = math.atan2(
            selfPos[1], selfPos[0]) - math.atan2(targetPos[1], targetPos[0])
        angleVector = angleVector * 360 / (2 * math.pi)

        if angleVector < 0:
            angleVector = angleVector + 360

        print "angleVector: ", angleVector

        if targetPos[0] == selfPos[0]:  # horizontally in line with each other
            print "targetPos[0] == self.x[0], angleVector: ", angleVector
            clock.tick(2000)

        """

        #angleVector = math.degrees(math.atan2(yDiff, xDiff))  #http://programarcadegames.com/python_examples/f.php?file=bullets_aimed.py
        angleVector = math.atan2(self.target.y, self.target.x) - math.atan2(self.y, self.x) #math.degrees()
        angleVector = angleVector * 360 / (2 * math.pi)
        if angleVector < 0:
            angleVector = angleVector + 360
        """

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

    """
    def angle_between(self, point1, point2):  #http://stackoverflow.com/a/31735642
        import numpy

        angle1 = numpy.arctan2(*point1[0])  # investigate  # *x is power?
        angle2 = numpy.arctan2(*point2[0])

        angleRad = (angle1 - angle2) % (2 * numpy.pi)

        return numpy.rad2deg(angleRad)  #rand2deg converts radeon to degrees
    """

    def length(self, v):
        import math

        return math.sqrt(v[0]**2 + v[1]**2)

    def dot_product(self, v, w):
        return v[0] * w[0] + v[1] * w[1]

    def determinant(self, v, w):
        return v[0] * w[1] - v[1] * w[0]

    def inner_angle(self, v, w):
        import math

        print "\ncreep: ", w
        cosx = self.dot_product(v, w) / (self.length(v) * self.length(w))
        rad = math.acos(cosx)  # in radians
        return rad * 180 / math.pi  # returns degrees

    def angle_clockwise(self, A, B):
        inner = self.inner_angle(A, B)
        det = self.determinant(A, B)
        inner = inner
        if det < 0:  # this is a property of the det. If the det < 0 then B is clockwise of A
            return inner
        else:  # if the det > 0 then A is immediately clockwise of B
            return (360 - inner)

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
