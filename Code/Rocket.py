from GlobalVars import surface, explosion_Sound  # this is necessary

import math
import pygame
pygame.init()


class Rocket(pygame.sprite.Sprite):
    # damage could probably be gotten from rocketTurret global
    def __init__(self, owner, target, direction, damage):

        super(Rocket, self).__init__()
        pygame.sprite.Sprite.__init__(self)

        self.frameCount = 0
        self.targetHit = False

        self.owner = owner
        self.target = target
        self.direction = direction
        if self.direction == "North":
            self.angle = 0
        elif self.direction == "East":
            self.angle = 90
        elif self.direction == "South":
            self.angle = 180
        elif self.direction == "West":
            self.angle = 270
        self.damage = damage

        self.size = [self.owner.size -
                     (self.owner.size / 2), self.owner.size + (self.owner.size / 2)]

        self.explosionSize = self.owner.explosionSize

        self.originalImage = pygame.image.load(
            "Graphics/Sprites/Towers/Rockets/Rocket.png").convert_alpha()
        self.originalImage = pygame.transform.scale(
            self.originalImage, (self.size[0], self.size[1]))
        self.image = self.originalImage
        self.rect = self.originalImage.get_rect()
        self.mask = pygame.mask.from_surface(self.originalImage)

        self.size = self.owner.size / 2  # half the size of a Rocketeer tower
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.x, self.y = self.owner.x, self.owner.y  # + 5, + 6  # or something

        ########################################################################

        self.speed = 3
        # self.magnitude = ???
        #self.topSpeed = 30  # Max speed in pixels per second
        self.rotAmount = 1

        self.deltax = self.target.x - self.x #difference in x of the bullet and creep
        self.deltay = self.target.y - self.y #difference in y of the bullet and creep

        self.velocity = [0, 0]
        self.velocity[0] = self.deltax/math.hypot(self.deltax, self.deltay)
        self.velocity[1] = self.deltay/math.hypot(self.deltax, self.deltay)

        self.acceleration = ((self.velocity[0]) * self.speed, (self.velocity[0]) * self.speed) #multiplied by the speed

    def rotate(self):
        self.image = self.originalImage
        newAngle = self.owner.getAngle(
            (self.x, self.y), (self.target.x, self.target.y))

        if self.angle + 5 >= newAngle >= self.angle - 5:
            self.image = self.originalImage
        else:
            if self.angle > newAngle:
                self.angle += self.rotAmount
            elif self.angle < newAngle:
                self.angle -= self.rotAmount
            # https://www.pygame.org/docs/ref/transform.html#pygame.transform.rotate
            # maybe should leave the rotation till after movement? maybe not?
            self.image = pygame.transform.rotate(
                self.originalImage, self.angle)

    def move(self):
        """
        self.velocity[0] = 15 * math.sin(self.angle)
        self.velocity[1] = 15 * math.cos(self.angle)
        """

        deltax = self.target.x - self.x
        deltay = self.target.y - self.y

        if deltax != 0:  # if rocketx == target.x
            self.velocity[0] = deltax/math.hypot(deltax, deltay)
        else:
            self.velocity[1] = 0

        if deltay != 0: # ""
            self.velocity[0] = deltay/math.hypot(deltax, deltay)
        else:
            self.velocity[1] = 0

        self.acceleration = ((self.velocity[0]) * self.speed, (self.velocity[1]) * self.speed)
        self.x += int(self.acceleration[0])
        self.y += int(self.acceleration[1])

        #self.x = self.x + self.velocity[0]
        #self.y = self.y + self.velocity[1]

    def rocketAftermath(self, initial):
        if initial == True:
            self.targetHit = True
            self.aftermathFrameCount = 1
            self.aftermathXCoord = self.x
            self.aftermathYCoord = self.y
            self.target.attacked(self.damage)
            pygame.mixer.Sound.play(explosion_Sound)
        elif self.aftermathFrameCount <= 34:  # during aftermath explosion  # 35 = self.aftermathFrameCount * 5
            explosion_Img = pygame.image.load(
                "Graphics/Sprites/Explosions/Explosion_%s.png" % (int(self.aftermathFrameCount / 5))).convert_alpha()
            explosion_Img = pygame.transform.scale(
                explosion_Img, (self.explosionSize, self.explosionSize))
            surface.blit(explosion_Img, (self.aftermathXCoord - (self.explosionSize / 4),
                                         self.aftermathYCoord - (self.explosionSize / 4)))
            self.aftermathFrameCount = self.aftermathFrameCount + 1
        else:  # aftermath explosion ends
            self.owner.rocket_List.remove(self)  # removes rocket object from rocket_List - effectively killing it


    def render(self):
        if self.targetHit == False:
            self.rotate()
            self.move()

            if self.target.x <= self.x <= (self.target.x + self.target.size) and self.target.y <= self.y <= (self.target.y + self.target.size):
                self.rocketAftermath(True)
            else:
                #self.frameCount % 3
                surface.blit(self.image, (self.x, self.y))
        if self.targetHit == True:
            self.rocketAftermath(False)

        #self.rect = self.image.get_rect()
        #self.mask = pygame.mask.from_surface(self.image)

        # maybe make mask collide?
        """
        if not pygame.sprite.collide_rect(self, self.target):
            surface.blit(self.image, (self.x, self.y))
            print "not colliding ---"
        else:
            print "=== colliding ==="
            self.target.attacked(self.damage)
            # TODO play explosion Sound
            # TODO play aftermath animation
            rocketIndex = self.owner.rocket_List.index(self)
            self.owner.rocket_List.pop(rocketIndex)
        """
