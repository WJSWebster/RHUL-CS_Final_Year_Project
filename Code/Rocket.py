import pygame
# pygame init()


class Rocket(pygame.sprite.Sprite):
    # damage could probably be gotten from rocketTurret global
    def __init__(self, owner, target, angle, damage):

        super(Rocket, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        print "new rocket created!"

        self.owner = owner
        self.target = target
        self.angle = angle
        self.damage = damage

        self.velocity = 0  # Current velocity in pixels per second
        # Pixels per second (Also applies as so called deceleration AKA
        # friction)
        self.acceleration = 1
        self.topSpeed = 30  # Max speed in pixels per second

        self.image = pygame.image.load("Graphics/Sprites/Other/Rocket.png")

        ###############################
        self.rect = self.image.get_rect()
        ###############################

        self.size = self.owner.size / 2  # half the size of a Rocketeer tower
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.x, self.y = self.owner.x, self.owner.y  # + 5, + 6  # or something

    def rotate(self):
        # pygame.transform.rotate(surface?, angle)
        # #https://www.pygame.org/docs/ref/transform.html#pygame.transform.rotate
        # https://docs.python.org/2/library/math.html#math.atan2
        self.angle = (self.target.x - self.x, self.target.y - self.y)

    def render(self):
        # if rotateFrame = frameCounter:
        self.rotate()
        # http://stackoverflow.com/questions/6775897/pygame-making-a-sprite-face-the-mouse
        rotatedImage = pygame.transform.rotate(self.image, self.angle)

        if not pygame.sprite.collide_rect(self.rect, self.target.rect):
            surface.blit(self.image, (self.x, self.y))
        else:
            self.target.attacked(self.damage)
            # play explosion Sound
            # play aftermath animation
            rocketIndex = rocket_List.index(self)
            rocket_List.pop(rocketIndex)
