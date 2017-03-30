#from GlobalVars import *
from GlobalVars import creep_List
import pygame
from pygame.sprite import Group
pygame.init()


class LaserObj(pygame.sprite.Sprite):
    def __init__(self, owner, x, y, direction, ownerSize):
        super(LaserObj, self).__init__()

        self.owner = owner
        self.x = x
        self.y = y
        self.direction = direction + 3  # seems slight off target for some reason?
        # TODO ^^Investigate

        self.ownerSize = ownerSize

        self.image = pygame.image.load(
            "Graphics/Sprites/Towers/Lasers/Laser_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (1200, 60))
        self.image = pygame.transform.rotozoom(
            self.image, -self.direction + 90, 0.5)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.laserX = (self.x + (self.ownerSize / 2)) - \
            (self.image.get_width() / 2)
        self.laserY = (self.y + (self.ownerSize / 2)) - \
            (self.image.get_height() / 2)

        self.collide_Group = Group()
        self.attackFrameCount = 0

    def attackCheck(self):
        self.collide_Group = Group()

        if self.attackFrameCount % 60 == 0:  # again, TODO need to change this to seperate variable attackFrameCount
            # TODO also, we need to make this so it's every 60 frames after the
            # initial hit on that creep
            for i in creep_List:
                # only any creeps not within range boundaries so cheaper to
                # mask colliside check
                if self.rect.colliderect(i.rect):
                    self.collide_Group.add(i)
            if len(self.collide_Group) > 0:
                maskCollide_List = pygame.sprite.spritecollide(
                    self, self.collide_Group, False, pygame.sprite.collide_mask)
                for i in maskCollide_List:  # TODO this attacks all that are in rect if only one is in mask!
                    i.attacked(self.owner.damage)  # appears to attack all creeps TODO fix!
                    print i, "mask collide!"
                    # self.collide_Group.remove(i)

        self.attackFrameCount += 1

    def render(self):
        from GlobalVars import surface

        laserFrame = int(self.attackFrameCount / 23)

        self.image = pygame.image.load(
            "Graphics/Sprites/Towers/Lasers/Laser_%s.png" % (laserFrame)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (1200, 60))
        self.image = pygame.transform.rotozoom(
            self.image, -self.direction + 90, 0.5)

        surface.blit(self.image, (self.laserX, self.laserY))

        # TODO may not need
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
