import pygame, math, random, sys#, simplegui

player_score = 0
lives_score = 3
boss_score = 50
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 800
background = simplegui.load_image(
    "http://www.nicewalpaper.com/wallpapers/space-blinking-of-stars-wallpapers-nice-wallpaper-1024x768.jpg")
background1X = CANVAS_WIDTH / 2
background2X = 0 - CANVAS_WIDTH / 2
gameover_Img = simplegui.load_image('https://db.tt/eK9DX3g7')

loc = (25, 35)
text_size = 40
gameover = False
BossHP = 20

ThrustersOn_Img = simplegui.load_image('http://i.imgur.com/CesnlLu.png')
ThrustersOff_Img = simplegui.load_image('http://i.imgur.com/ZWqbTkr.png')
ThrustersTurnL_Img = simplegui.load_image('http://i.imgur.com/FyCEpWA.png')
ThrustersTurnR_Img = simplegui.load_image('http://i.imgur.com/Fg3oisg.png')

astSprite_Img = simplegui.load_image(
    'http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png')
asteroidField = set()
asteroidlimit = 5

laser_Img = simplegui.load_image('https://db.tt/1POAs6oD')
laserGroup = set()

Splash_Img = simplegui.load_image('https://db.tt/LgQG9wOf')
gamestart = False

boss = None
boss_score = 0

NunoHappy_Img = simplegui.load_image('https://db.tt/K0AdARe2')
NunoAngry_Img = simplegui.load_image('https://db.tt/PVOdgecK')
NunoShoot_Img = simplegui.load_image('https://db.tt/6yeAsjFl')
bossFace = NunoHappy_Img

gameMusic = simplegui.load_sound('https://dl.dropboxusercontent.com/u/96602750/spacey.mp3')
gameMusic.set_volume(0.0)  # (0.7)
gameMusic.play()

def main():
    frame()


def frame(): #used for changing from simplegui to pygame

def vecTrig(angle):
    return [math.cos(ang), math.sin(ang)]


class Vector:
    # Initialiser
    def __init__(self, x=0, y=0, rot=0, v=0):
        self.x = x
        self.y = y
        self.v = 0
        self.rotation_v = 0

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

    # Adds another vector to this vector
    def add(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self

    def length(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def sub(self, other):
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self

    def copy(self):
        copyX = self.x
        copyY = self.y

        return Vector(copyX, copyY)


class Sprite:
    def __init__(self, image, center, dimensions, position,
                 destDim, angle, radius=0, velocity=0):
        self.rot = 0;
        self.rot_Travel = 0
        self.img = image
        self.center = center
        self.dim = dimensions
        self.p = position
        self.destDim = destDim
        self.r = (1.30 * (math.pow(destDim[0] * destDim[1], 0.625) / math.pow(destDim[0] + destDim[1], 0.25))) / 2
        self.v = velocity
        self.rotation_v = 0
        self.goFowards = False
        self.angle = angle
        self.laser_despawn = -100

    def update(self):
        if not self.laser_despawn == -1:
            self.laser_despawn -= 1

        self.p.add(Vector(self.v * math.cos(self.rot_Travel), self.v * math.sin(self.rot_Travel)))
        outer_barriers()
        self.rot += self.rotation_v

        return self

    def rotation_vPlus(self, on=True):
        if on:
            self.rotation_v += 0.05
        else:
            self.rotation_v = 0

    def rotation_vMinus(self, on=True):
        if on:
            self.rotation_v -= 0.05
        else:
            self.rotation_v = 0

    def draw(self, canvas):
        canvas.draw_image(self.img, self.center, self.dim,
                          (self.p.x, self.p.y), self.destDim, self.rot)

    def shoot(self):
        global missile

        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile = Sprite('http://www.defcom1.net/xnalessons/laser.png'(missile_pos, missile_vel, self.angle, 0))

    def inside(self, p, r):
        temp = self.p.copy()
        temp.sub(p)
        return temp.length() < (self.r + r)


class Key:
    def __init__(self, keyName):
        self.key = simplegui.KEY_MAP[keyName]
        self.isPressed = False

    def isKey(self, pressedKey):
        return self.key == pressedKey

    def press(self):
        self.isPressed = True

    def release(self):
        self.isPressed = False


# Global variables
v1 = Vector(0, 0)
v2 = Vector(0, 0)
v3 = (3, 2)
step = 4
# Sprite initial position
p = Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
p1 = Vector(5, CANVAS_HEIGHT / 2)
p2 = Vector(CANVAS_WIDTH, CANVAS_HEIGHT / 2)

up = Key('up')
down = Key('down')
right = Key('right')
left = Key('left')
space = Key('space')

Ship = Sprite(ThrustersOff_Img,
              (299, 177), (598, 354), p.copy(), (120, 60), 40)


def checkInside():
    global asteroidField, laserGroup, Ship, lives_score, player_score, boss, BossHP

    for obj in asteroidField:
        if Ship.inside(obj.p, (obj.r - 20)):
            asteroidField.remove(obj)
            lives_score -= 1
            Ship.p = p.copy()

    for laser in laserGroup:
        for asteroid in asteroidField:
            if laser.inside(asteroid.p, (asteroid.r - 20)):
                laserGroup.remove(laser)
                asteroidField.remove(asteroid)
                player_score += 1

    if boss is not None:
        if Ship.inside(boss.p, (boss.r - 20)):
            lives_score -= 1
            Ship.p = p.copy()

        for obj in laserGroup:
            if laser.inside(boss.p, (boss.r - 20)):
                BossHP -= 1
                timer = simplegui.create_timer(500, nunoHit)
                # timer.start()
                temp = boss.v
                boss.img = NunoAngry_Img
                boss.v = temp
                boss.v += 0.5
                laserGroup.pop()


def nunoHit():
    bossFace = NunoShoot_Img


def ticker():
    if gameover == False:
        timer = simplegui.create_timer(1000, Asteroid_Spawner)  # maybe change length
        if (len(asteroidField) < asteroidlimit):
            timer.start()


def Bossteroid():
    global boss
    asteroidlimit = 0
    for obj in asteroidField:
        asteroidField.pop()
    new_aPosX = random.randrange(10, 690)
    new_aPosY = random.randrange(10, 690)

    if boss is None:
        boss = Sprite(bossFace,
                      (236 / 2, 267 / 2), (236, 267), Vector(new_aPosX, new_aPosY), (200, 200), 40)
        boss.v = 1.5
        boss.rot_Travel = random.random() * 10

    if ((boss.p.y) < 0 + 267 / 2):
        boss.rot_Travel += math.pi
    if ((boss.p.y) > CANVAS_HEIGHT - 307 / 2):
        boss.rot_Travel += math.pi
    if ((boss.p.x) > CANVAS_WIDTH - 276 / 2):
        boss.rot_Travel += math.pi
    if ((boss.p.x) < 0 + 236 / 2):
        boss.rot_Travel += math.pi


def drawHandler(c):
    global Ship, asteroidField, laserGroup, background1X, background2X, gameover, boss
    # Background draw:
    background1X += 1
    background2X += 1
    c.draw_image(background, (633 / 2, 475 / 2), (633, 475), (background1X, CANVAS_HEIGHT / 2),
                 (CANVAS_WIDTH, CANVAS_HEIGHT))
    c.draw_image(background, (633 / 2, 475 / 2), (633, 475), (background2X, CANVAS_HEIGHT / 2),
                 (CANVAS_WIDTH, CANVAS_HEIGHT))
    if (background1X == CANVAS_WIDTH * 1.5):
        background1X = 0 - CANVAS_WIDTH / 2
    if (background2X == CANVAS_WIDTH * 1.5):
        background2X = 0 - CANVAS_WIDTH / 2

    checkInside()

    for obj in laserGroup:
        obj.update()
        obj.draw(c)

    temp = set(laserGroup)
    for obj in laserGroup:
        if obj.laser_despawn == 0:
            temp.pop(obj)
    laserGroup = temp.copy()

    Ship.update()
    Ship.draw(c)

    if boss is not None:
        boss.update()
        boss.draw(c)
    else:
        for obj in asteroidField:
            obj.update()
            obj.draw(c)

    c.draw_text("Score: " + str(player_score), (CANVAS_WIDTH / 3, 25), 22, "Yellow", "sans-serif")
    if (lives_score == 3):
        c.draw_text("Lives: " + str(lives_score), ((CANVAS_WIDTH / 3) * 2, 25), 22, "White", "sans-serif")
    elif (lives_score < 3):
        c.draw_text("Lives: " + str(lives_score), ((CANVAS_WIDTH / 3) * 2, 25), 22, "Red", "sans-serif")

    if (gamestart == False):
        c.draw_image(Splash_Img, (1800 / 2, 1600 / 2), (1800, 1600), (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2),
                     (CANVAS_WIDTH, CANVAS_HEIGHT))

    if lives_score < 1:
        c.draw_image(gameover_Img,
                     (1800 / 2, 1600 / 2), (1800, 1600), (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2),
                     (CANVAS_WIDTH, CANVAS_HEIGHT))
        for obj in asteroidField:
            asteroidField.pop()
        asteroidlimit = 0
        gameover = True
    if player_score == 10:
        Bossteroid()
        c.draw_text("Bossteroid Health: " + str(BossHP), (CANVAS_WIDTH / 2, 55), 22, "Red", "sans-serif")


def laserTick(currentKey):
    if gameover == False:
        laserTimer = simplegui.create_timer(1000, laser_stop)


def Asteroid_Spawner():
    global asteroidlimit
    new_aPosX = random.randrange(0, 700)  # make dynamic
    new_aPosY = random.randrange(0, 700)
    ran_Size = random.randrange(60, 130)
    # ran new_asize
    Asteroid = Sprite(astSprite_Img,
                      (45, 45), (90, 90), Vector(new_aPosX, new_aPosY), (ran_Size, ran_Size),
                      40)  # replace with new_asize

    Asteroid.v = random.random() + 0.5
    Asteroid.rot_Travel = random.random() * 10
    if len(asteroidField) < asteroidlimit:
        asteroidField.add(Asteroid)
    else:
        pass
        # print len(asteroidField) #(DEBUG)


def Laser_Spawner():
    # ran new_asize
    laser = Sprite(laser_Img,
                   (509 / 2, 475 / 2), (509, 475), Ship.p.copy(), (509 / 12, 475 / 8), 40)  # replace with new_asize
    laser.v = 7
    laser.rot_Travel = Ship.rot
    laser.rot = Ship.rot
    laser.laser_despawn = 60 * 2

    if (len(laserGroup) < 20):
        laserGroup.add(laser)
    # need a way of popping bottom laser after a certain timer
    print len(laserGroup)  # (DEBUG)


def laser_stop():
    laserGroup.pop()


def startGame():
    global gamestart
    gamestart = True


def keyDownHandler(currentKey):
    if gameover == False:
        if up.isKey(currentKey):
            Ship.img = ThrustersOn_Img
            Ship.rot_Travel = Ship.rot
            Ship.goForwards = True
            Ship.v = 3.5
            # gamestart = True
            timer = simplegui.create_timer(1000, startGame)
            timer.start()

        if left.isKey(currentKey):
            # animation
            Ship.img = ThrustersTurnL_Img
            Ship.rotation_vMinus()

        if right.isKey(currentKey):
            # animation
            Direction = Ship.rot
            Ship.img = ThrustersTurnR_Img
            Ship.rotation_vPlus()

        if space.isKey(currentKey):
            Laser_Spawner()


def keyUpHandler(currentKey):
    if gameover == False:
        if currentKey == simplegui.KEY_MAP['up']:
            Ship.img = ThrustersOff_Img
            Ship.v = 1
            constantVel = Ship.v

        if currentKey == simplegui.KEY_MAP['left']:
            Ship.rotation_vMinus(False)
            # animation
            Ship.img = ThrustersOff_Img

        if currentKey == simplegui.KEY_MAP['right']:
            Ship.rotation_vPlus(False)
            # animation
            Ship.img = ThrustersOff_Img


def outer_barriers():
    if Ship.p.x > (CANVAS_WIDTH + 60):
        Ship.p.x = (0 - 60)
    if Ship.p.x < (0 - 60):
        Ship.p.x = (CANVAS_WIDTH + 60)
    if Ship.p.y > (CANVAS_HEIGHT + 60):
        Ship.p.y = (0 - 60)
    if Ship.p.y < (0 - 60):
        Ship.p.y = (CANVAS_HEIGHT + 60)

    for obj in asteroidField:
        if obj.p.x > (CANVAS_WIDTH + 40):
            obj.p.x = (0 - 40)
        if obj.p.x < (0 - 40):
            obj.p.x = (CANVAS_WIDTH + 40)
        if obj.p.y > (CANVAS_HEIGHT + 40):
            obj.p.y = (0 - 40)
        if obj.p.y < (0 - 40):
            obj.p.y = (CANVAS_HEIGHT + 40)


def tog_start():
    global player_score, lives_score, Ship
    Ship.p.x = (CANVAS_WIDTH / 2)
    Ship.p.y = (CANVAS_HEIGHT / 2)
    Ship.v = 0
    Ship.rot = math.radians(0)
    player_score = 0
    lives_score = 3
    gameover == False
    for obj in asteroidField:
        asteroidField.pop()
    gameMusic.rewind()
    gameMusic.play()
    for obj in laserGroup:
        laserGroup.pop()


def difEasy():
    global asteroidlimit, boss_score
    asteroidlimit = 5
    boss_score = 20
    bossHP = 5
    tog_start()


def difMedium():
    global asteroidlimit, boss_score
    asteroidlimit = 10
    boss_score = 25
    bossHP = 10
    tog_start()


def difHard():
    global asteroidlimit, boss_score
    asteroidlimit = 15
    boss_score = 30
    bossHP = 15
    tog_start()


def difInsane():
    global asteroidlimit, boss_score
    asteroidlimit = 20
    boss_score = 35
    bossHP = 20
    tog_start()


def Quit_Game():
    gameMusic.pause()
    sys.exit()


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Asteroids Game!!", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(drawHandler)
frame.set_keyup_handler(keyUpHandler)
frame.set_keydown_handler(keyDownHandler)
frame.add_button("Re-start?", tog_start, 100)
frame.add_button("Easy", difEasy, 100)
frame.add_button("Medium", difMedium, 100)
frame.add_button("Hard", difHard, 100)
frame.add_button("Insane", difInsane, 100)
frame.add_button("Quit Game", Quit_Game, 100)

# Collision
# checkInside()
# Timer for spawner
ticker()
# Start the frame animation
frame.start()
