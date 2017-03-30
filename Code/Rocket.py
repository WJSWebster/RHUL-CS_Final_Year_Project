from GlobalVars import surface  # this is necessary

import math
import pygame
pygame.init()


class Rocket(pygame.sprite.Sprite):
    # damage could probably be gotten from rocketTurret global
    def __init__(self, owner, target, direction, damage):

        super(Rocket, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        print "new rocket created!"

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

        self.velocity = [1, 1]  # Current velocity in pixels per second
        self.acceleration = 1
        # self.magnitude = ???
        self.topSpeed = 30  # Max speed in pixels per second
        self.rotAmount = 1

        self.size = [self.owner.size -
                     (self.owner.size / 2), self.owner.size + (self.owner.size / 2)]

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
        self.velocity[0] = 15 * math.sin(self.angle)
        self.velocity[1] = 15 * math.cos(self.angle)

        self.x = self.x + self.velocity[0]
        self.y = self.y + self.velocity[1]

    def render(self):
        # TODO if attackFrameCount % ?? == ??:
        self.rotate()
        self.move()

        surface.blit(self.image, (self.x, self.y))

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

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
