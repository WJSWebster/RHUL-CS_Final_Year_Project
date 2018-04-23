from GlobalVars import death_List
import pygame
from Creep import *

pygame.init()


class Tunneller(Creep):
    def __init__(self, x, y):
        # super(Creep, self).__init__()  # TODO researc into derived classes
        #super(Tunneller, self).__init__()
        # pygame.sprite.Sprite.__init__(self)
        Creep.__init__(self, x, y, 2)

        self.x = int(x)
        self.y = int(y)

        self.size = 28
        self.direction = 'West'

        self.flagNo = 0
        self.pathComplete = False

        self.speciesNo = 2
        self.species, self.health, self.damage, self.speed, self.cost = Creep.getSpecies(
            self.speciesNo)

        self.target = [0, 0]
        self.shortcutFlagCoords = self.getShortCutFlagCoords()

        # only for attackedText function
        self.attackedFrameCount = None
        self.attackedXCoord = None
        self.attackedYCoord = None
        self.attackedDamageAmount = None

        def getSpecies(self, speciesNo):  # should be derived from Creep class
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

    def getShortCutFlagCoords(self):
        from GlobalVars import death_List

        print "\nTunneller initial death_List: ", death_List

        for i in death_List:  # find the path with the highest concentration of creep deaths
            if self.target[1] < i[1]:
                print "higher target found - updating target from %s to %s." % (self.target, i)
                self.target = i

        self.target = self.target[0]
        print "target flag = ", self.target

        j = 0

        shortcut = []  # a list of two tupes, the shortcut start and end coords - only local as returned at end of method back to init for attribute assignment

        for i in (-1, 1):  # once for before and after the target path
            flag1 = main.getFlagCoords(self.target + i)  # either -1 or 1
            flag2 = main.getFlagCoords(self.target + (i + 1))  # either 0 or 2

            if flag1[0] != flag2[0]:  # x coords not equal, therefore path movement along y axis
                dim = 0  # dim aka dimension - 0 = x axis, 1 = y axis
            else:
                dim = 1

            if flag2[dim] > flag1[dim]:  # path is going up or right
                flag2Greater = True
                pathDiff = (flag2[dim] - flag1[dim])
            else:  # TODO possibly replace this whole if block with an if 'pathDiff = -int: ' catch
                flag2Greater = False
                pathDiff = (flag1[dim] - flag2[dim])

            halfPathDiff = pathDiff / 2

            if not (halfPathDiff).is_integer():  # if halfPathDiff not whole number
                if flag2Greater:
                    # rounds number down - int() as math.floor returns float
                    halfPathDiff = int((math.floor(halfPathDiff)))
                else:
                    # rounds number up - ""
                    halfPathDiff = int((math.ceil(halfPathDiff)))

            if halfPathDiff % 2 == 0:
                if flag2Greater:
                    # such that shortcut is always further away from target
                    # path
                    halfPathDiff = flag1[dim] + (halfPathDiff - 1)
                else:
                    halfPathDiff = flag2[dim] + (halfPathDiff + 1)

            for k in range(2):
                if k == dim:
                    shortcut[j][k] = halfPathDiff
                else:
                    shortcut[j][k] = flag1[j]  # or flag2, it doesnt matter

            j += 1

        print "shortcut = ", shortcut
        return shortcut

    def getShortCutPath(self):
        pass
        # if not shortcutPath[0][0] == shortcutPath[1][0]:  # x coordinates not equal, so need to change direction half way through shortcutPath
        # else if not shortcutPath[0][1] == shortcutPath[1][1]:  # y coords not equal, " "
        # else:  # path between the two is a straight line

        # TODO use A* algorithm or something else from robotics
        # http://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/
