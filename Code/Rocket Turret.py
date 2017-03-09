from main import surface, entitySelected, creep_List
import pygame

class Rocketeer(pygame.sprite.Sprite):  # need to make derived from turret class
    def __init__(self, x, y, hover):  # maybe not needed, as seen above ^^
        #from main import creep_List
        pygame.sprite.Sprite.__init__(self)

        self.typeNo = 2
		self.type, self.damage, self.attackSpeed, self.cost = self.getType()
        self.x, self.y = x, y

        self.size = 28
        self.hover = hover  # most likely True?

	def getType(self):
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
			elif "[%s]" % (typeNo + 1)in line:
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
            print "creep_List[0]: ",creep_List[0]
            self.target = creep_List[0]
            print "target", self.target
            return True
        else:
            print self, "no creeps in creep_List"
            return False

    def rocketAttack(self):  # could also be joined to attack method once class is derived
        if not self.attacking:
            if self.targetFinder():
                #print "target: ", self.target
        # ~~~Continue later~~~~
