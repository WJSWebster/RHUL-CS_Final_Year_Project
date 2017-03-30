import pygame
from pygame.locals import *
from pygame.sprite import Group, collide_mask
pygame.init()

# Assigns the width and height of the screen as a tuple
canvas_width = 1000
canvas_height = 800
canvas_dimensions = (canvas_width, canvas_height)
surface = pygame.display.set_mode(canvas_dimensions)  # , FULLSCREEN

pygame.display.set_caption("Collision Test")

# Manages how frequently surface updates ('flips')
clock = pygame.time.Clock()
fps = 60

white = (255, 255, 255)
red = (200, 0, 0)


def testLoop():
    frameCounter = 0

    # The location of the mouse cursor on screen and the state of each mouse
    # button (re-assigned each loop)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    box_List = []
    box_Group = Group()
    ranger_List = []
    ranger_Group = Group()

    boxObj = Box(True)  # makes it a sprite
    box_List.append(boxObj)

    rangerObj = Ranger(True)  # makes it a sprite
    ranger_List.append(rangerObj)

    if boxObj.sprite:
        box_Group.add(boxObj)
    if rangerObj.sprite:
        ranger.Group.add(rangerObj)

    # pygame.mouse.set_visible(False)

    while True:
        # The location of the mouse cursor on screen and the state of each mouse
        # button (re-assigned each loop)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        surface.fill(white)

        if rangerObj.sprite:
            creep_Mask = pygame.mask.from_surface(rangerObj.image)

        boxObj.render()
        rangerObj.render()

        if boxObj.sprite and rangerObj.sprite:
            if pygame.sprite.spritecollide(boxObj, rangerObj, False):
                print "spritecollide!"

            print "collide_mask(): ", pygame.sprite.collide_mask(rangerObj, boxObj)
            print "spritecollide: ", pygame.sprite.spritecollide(rangerObj, box_Group, False, pygame.sprite.collide_mask)

        if boxObj.sprite:
            if pygame.sprite.spritecollide(boxObj, circle, False, collide_circle):
                print "spritecollide - collide_circle!"

        if click[0] == 1:  # if left mouse button is being pressed down
            rangerObj.mask.fill()
            boxObj.mask.fill()

        print "collide_mask(): ", pygame.sprite.collide_mask(rangerObj, boxObj)

        print "spritecollide: ", pygame.sprite.spritecollide(rangerObj, box_Group, False, pygame.sprite.collide_mask)

        if frameCounter % 60 == 0:
            target_List = []
            for i in creep_List:
                if rangerObj.rect.colliderect(i.rect):
                    collide_Group.add(i)
            if len(collide_Group) > 0:
                if pygame.sprite.spritecollide(rangerObj, creep_group, False, pygame.sprite.collide_mask):
                    print "mask collide!"

        # limits surface update rate to a maximum of 60 frames per second
        clock.tick(fps)
        # Pygame function to update surface with what has been blit-ed
        pygame.display.flip()


class Box(pygame.sprite.Sprite):
    def __init__(self, sprite=False):

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        self.x = mouse[0]
        self.y = mouse[1]

        self.size = 28
        self.sprite = sprite

        if self.sprite:
            self.image = pygame.image.load(
                "Graphics/Protractor.png").convert_alpha()
            self.image = pygame.transform.scale(
                self.image, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.circle = pygame.draw.rect(
                surface, red, (self.x, self.y, self.size, self.size))
            # self.rect = self.circle.get_rect()  # AttributeError: 'pygame.Rect' object has no attribute 'get_rect'
            # self.mask = pygame.mask.from_surface(self.circle)  # TypeError:
            # argument 1 must be pygame.Surface, not pygame.Rect

    def render(self):
        if self.sprite:
            surface.blit(self.image(self.x, self.y))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.circle = pygame.draw.rect(
                surface, red, (self.x, self.y, self.size, self.size))
            # self.rect = self.circle.get_rect()  # AttributeError: 'pygame.Rect' object has no attribute 'get_rect'
            # self.mask = pygame.mask.from_surface(self.circle)   # TypeError:
            # argument 1 must be pygame.Surface, not pygame.Rect


class Ranger(pygame.sprite.Sprite):
    def __init__(self, sprite=False):
        self.x = canvas_width / 2
        self.y = canvas_height / 2

        self.size = 100
        self.sprite = sprite

        if self.sprite:
            self.image = pygame.image.load(
                "Graphics/Protractor.png").convert_alpha()
            self.image = pygame.transform.scale(
                self.image, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.circle = pygame.draw.rect(
                surface, red, (self.x, self.y, self.size, self.size))
            # self.rect = self.circle.get_rect()  # AttributeError: 'pygame.Rect' object has no attribute 'get_rect'
            # self.mask = pygame.mask.from_surface(self.circle)  # TypeError:
            # argument 1 must be pygame.Surface, not pygame.Rect

    def render(self):
        if self.sprite:
            surface.blit(self.image(self.x, self.y))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.circle = pygame.draw.rect(
                surface, red, (self.x, self.y, self.size, self.size))
            # self.rect = self.circle.get_rect()  # AttributeError: 'pygame.Rect' object has no attribute 'get_rect'
            # self.mask = pygame.mask.from_surface(self.circle)  # TypeError:
            # argument 1 must be pygame.Surface, not pygame.Rect


testLoop()
