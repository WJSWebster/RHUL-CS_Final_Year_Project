from GlobalVars import surface, entitySelected, explosion_Sound, red, creep_List
#from main import creep_List
# import Creep
import pygame
pygame.init()


# may make this a basic class from which other tower types are derived
# from (ie, "Cannon" or "Rocketeer")
class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, hover):

        super(Tower, self).__init__()
        pygame.sprite.Sprite.__init__(self)

        self.typeNo = 1
        self.type, self.damage, self.cooldownTime, self.radius, self.cost = self.getType()
        self.x, self.y = x, y

        self.size = 28
        # self.target = creep_List[0]
        self.direction = None
        self.hover = hover   # most likely True?

        self.image = pygame.image.load("Graphics/Sprites/Towers/Cannon_NS_Idol.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.range_Img = pygame.image.load(
            "Graphics/Sprites/Towers/Range/RangeCircle.png").convert_alpha()
        self.range_Img = pygame.transform.scale(self.range_Img, (self.radius, self.radius))
        self.rangeCirclePos = (self.x - (self.radius / 2), self.y - (self.radius / 2))


        self.attacking = False
        # self.cooldownTime = 120  # dependent on tower
        self.attackFrameCount = 0
        self.cooldownTimeFrameCount = 0 # currently not used with Cannon but TODO will in future
        self.target = None
        self.targetXInitial = None  # Canon only
        self.targetYInitial = None  # Canon only
        self.shadow_Img = pygame.image.load(
            "Graphics/Sprites/Towers/Cannon/Shadow.png").convert_alpha()
        self.cannonBall_Img = pygame.transform.scale(pygame.image.load(
            "Graphics/Sprites/Towers/Cannon/CannonBall.png").convert_alpha(), (self.size, self.size))
        # self.explosion_Img = pygame.transform.scale(pygame.image.load("Graphics/Sprites/Other/Explosion.png").convert_alpha(), (self.size, self.size).convert())

        self.radius_Img = pygame.image.load(
            "Graphics/RadiusMask.png")  # .convert_alpha()

        self.explosionSize = int(self.size * 2)
        self.aftermathFrameCount = 0
        self.aftermathXCoord = None
        self.aftermathYCoord = None
        self.aftermathBool = False

    def getType(self):
        typeFile = open("Types.txt", 'r')

        parsing = False

        for line in typeFile:
            if"[%s]" % (self.typeNo) in line:
                typeName = line.split("] ")[1].split(":")[0]
                parsing = True
            elif parsing and "Damage =" in line:
                damage = line.split(" = ")[1]
            elif parsing and "Cooldown Time =" in line:
                cooldownTime = line.split(" = ")[1]
            elif parsing and "Radius =" in line:
                radius = line.split(" = ")[1]
            elif parsing and "Cost =" in line:
                cost = line.split(" = ")[1]
            elif "[%s]" % (self.typeNo + 1) in line:
                parsing = False
                break
            """
            elif parsing and "Splash Damage =" in line:
                splashDamage = line.split(" = ")[1]
            """

        typeFile.close()
        return (typeName, int(damage), int(cooldownTime), int(radius), int(cost))

    def targetFinder(self):
        #from main import creep_List

        #self.radius_Img = pygame.draw.circle(surface, red, (self.x, self.y), self.radius)
        """
        target_List = pygame.sprite.spritecollide(self.radius_Img, creep_List, False, pygame.sprite.collide_circle
        print "target_List: ", target_List
        """

        """self.radius_Img = (pygame.mask.from_threshold(self.radius_Img, (0, 255, 255),
                               (0, 0, 0, 255), None, 1)
        """
        """
        for i in creep_List:
            if pygame.sprite.collide_mask(self.radius_Img, i):
                print "collide"
        """

        """
        self.radius_Img = pygame.mask.from_surface(self.radius_Img)

        for i in creep_List:
            if pygame.mask.from_surface(self.radius_Img).colliderect(i.rect):
                print "collide2"
        """

        #http://www.cogsci.rpi.edu/~destem/gamedev/pygame.pdf

        # wont even be tested unless attacking is False (pointless?)
        """
        if not self.attacking:
            target_List = self.checkRange(self)
            if target_List != False:
                self.target = target_List[0]
                return True
            else:
                return False
            """
        print "targetFinder: creep_List: ", creep_List

        if len(creep_List) != 0:
            self.target = creep_List[0]
            print "Tower target found!: ", self.target
            return True
        else:
            print "no creep found"
            return False
            """
                for i in creep_List:
                    if hasattr(i, 'image'):
                        collision = pygame.sprite.collide_mask(
                            self.radius_Img, i.image)
                        if collision:
                            print "\nTARGET FOUND\n"
                            self.target = i
                        # append target list?
                        break
                        return True
                    # creep not yet fully initialised (no rect attribute yet)
                    else:
                        pass
                    # self.target = creep_List[0]

                else:  # no creeps in range
                    return False

            return True
        else:
            return False
        # note: creep_List[0] means that the target is always the one at the
        # front TODO add turret behaviour options (ie, target strongest)


		# need a section to account for creep speed, time of projectile and possible corners
		"""

    def cannonBallAttack(self):
        # TODO look into this and other examples of redundent(mulitple) imports
        # of same variables
        from main import explosion_Sound
        if not self.attacking:
            if self.targetFinder():
                #print "Tower target:", self.target  #DEBUG

                self.targetXInitial, self.targetYInitial = self.target.x, self.target.y
                self.attacking = True
                # re-assigned at the beginning (maybe?)
                self.attackFrameCount = 1
        else:
            if self.attackFrameCount == self.cooldownTime:  # attack frame
                pygame.mixer.Sound.play(explosion_Sound)
                self.target.attacked(self.damage)
                self.cannonBallAftermath(
                    self.targetXInitial, self.targetYInitial)
                self.attacking = False
                self.target, self.targetXInitial, self.targetYInitial = None, None, None
            elif self.attackFrameCount < self.cooldownTime:  # attack coming
                sizeMultiplied = int(
                    self.size + (self.size - ((float(self.attackFrameCount) / self.cooldownTime) * self.size)))
                fallDistance = float(
                    (self.cooldownTime - self.attackFrameCount) / 0.25)

                shadow_Img = pygame.transform.scale(
                    self.shadow_Img, (sizeMultiplied, sizeMultiplied))
                surface.blit(shadow_Img, (self.targetXInitial - (sizeMultiplied / 5),
                                          self.targetYInitial - (sizeMultiplied / 5)))
                surface.blit(self.cannonBall_Img, (self.targetXInitial,
                                                   (self.targetYInitial - fallDistance)))
                self.attackFrameCount = self.attackFrameCount + 1

    def cannonBallAftermath(self, aftermathXCoord=None, aftermathYCoord=None):
        if aftermathXCoord != None and aftermathYCoord != None:  # new aftermath being initialised
            self.aftermathFrameCount = 1
            self.aftermathXCoord = aftermathXCoord
            self.aftermathYCoord = aftermathYCoord
            self.aftermathBool = True
        if self.aftermathFrameCount <= 34:  # during aftermath explosion  # 35 = self.aftermathFrameCount * 5
            explosion_Img = pygame.image.load(
                "Graphics/Sprites/Explosions/Explosion_%s.png" % (int(self.aftermathFrameCount / 5))).convert_alpha()
            explosion_Img = pygame.transform.scale(
                explosion_Img, (self.explosionSize, self.explosionSize))
            surface.blit(explosion_Img, (self.aftermathXCoord - (self.explosionSize / 4),
                                         self.aftermathYCoord - (self.explosionSize / 4)))
            self.aftermathFrameCount = self.aftermathFrameCount + 1
        else:  # aftermath explosion ends
            self.aftermathBool = False
            self.aftermathXCoord = None  # back to __init__ state
            self.aftermathYCoord = None

    def render(self, xCoord=None, yCoord=None):
        if self.hover:
            self.image = pygame.image.load(
                "Graphics/Sprites/Towers/Cannon_Transparent.png").convert_alpha()
            pygame.mouse.set_visible(False)
            # pygame.mouse.set_cursor  #
            # https://www.pygame.org/docs/ref/mouse.html#pygame.mouse.set_cursor
        else:
            # self.cannonBallAttack()
            if self.direction == None:  # placeholder, may replace whole sprite with cannon sprite
                if self.cooldownTime - 6 <= self.attackFrameCount  <= self.cooldownTime:
                    self.image = pygame.image.load(
                        "Graphics/Sprites/Towers/Cannon_NS_Firing.png").convert_alpha()
                else:
                    self.image = pygame.image.load("Graphics/Sprites/Towers/Cannon_NS_Idol.png").convert_alpha()
                    # TODO implement W & E Cannon
            else:
                self.image = pygame.image.load(
                    "Graphics/Sprites/Towers/Cannon_%s_Idol.png" % (self.direction)).convert_alpha()

        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        if xCoord == None and yCoord == None:  # rendering on game map
            surface.blit(self.image, (self.x, self.y))

            if entitySelected == self:
                surface.blit(self.range_Img, self.rangeCirclePos)

                silhouette_Img = pygame.image.load(
                    "Graphics/Sprites/Towers/TowerSilhouette.png").convert_alpha()
                silhouette_Img = pygame.transform.scale(
                    silhouette_Img, (self.size, self.size))
                surface.blit(silhouette_Img, (self.x, self.y))

            # and if tower of type [1]
            if not self.hover:
                self.cannonBallAttack()
        else:
            surface.blit(self.image, (xCoord, yCoord))

        if self.aftermathBool:
            self.cannonBallAftermath()

    def checkRange(self, tower):
        from main import creep_List
        ####  - not necessary, but used for illustrative purposes
        rangeCirclePos = (tower.x - (tower.radius / 2), tower.y - (tower.radius / 2))
        range_Img = pygame.image.load(
            "Graphics/Sprites/Towers/Range/RangeCircle.png").convert_alpha()  # TODO should be pulled from derived class (Tower)
        range_Img = pygame.transform.scale(range_Img, (tower.radius, tower.radius))
        #surface.blit(range_Img, rangeCirclePos)
        #pygame.draw.circle(surface, red, rangeCirclePos, tower.radius)
        pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        #########################################

        target_List = []

        if len(creep_List) > 0:
            for i in creep_List:
                if pygame.sprite.collide_circle(tower, i):
                    print i, "is in range of tower ", tower
                    target_List.append(i)
            else:
                print "no creeps detected!"
        else:
            print "creep list is empty"
        if len(target_List) > 0:
            return target_List
        else:
            return False

    # not actually used by cannon (so should move cannon into it's own class),
    # but is used by Rocketeer and Laser
    def getAngle(self, centre, target): # http://stackoverflow.com/a/42258870
        import math

        radAng = math.atan2(target[1] - centre[1], target[0] - centre[0])

        degAng = math.degrees(radAng)

        if degAng < 0:  # fixes output of degrees between -180 and 180
            degAng = degAng + 360

        # 'rotates' the origin (or 0*) point to backwards 90*
        degAng = degAng + 90

        # accounts for previous calibration, so that any angle above 360 (ie,
        # north - origin point) is set to zero and upwards to 90
        if degAng >= 360:
            degAng = degAng - 360

        # This then, creates a clockwise angle readout from 0-359.99 in degrees

        return degAng
