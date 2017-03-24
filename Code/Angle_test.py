import math
import sys
import pygame

pygame.init()

# from GlobalVars import *
# from __init__ import *

# Assigns the width and height of the screen as a tuple
canvas_width = 1000
canvas_height = 800
canvas_dimensions = (canvas_width, canvas_height)
surface = pygame.display.set_mode(canvas_dimensions)  # , FULLSCREEN

pygame.display.set_caption("Angle Test")

# Manages how frequently surface updates ('flips')
clock = pygame.time.Clock()
fps = 60

# The location of the mouse cursor on screen and the state of each mouse
# button (re-assigned each loop)
mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed()

protractor_Img = pygame.image.load("Graphics/Protractor2.png").convert_alpha()
protractor_Img = pygame.transform.scale(protractor_Img, (800, 800))
protractor_Img = pygame.transform.rotate(protractor_Img, -90)

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)

smallText = pygame.font.SysFont('ubuntu', 20)  # 'ubuntu'

button_State = 0

prevMousePos = (0, 0)

protCentre = (500, 400)

A = (1, 0)
B = (1, -1)


def displayText(text, font, colour, centX, centY):
    if "\n" in text:
        halfFontSize = font.get_linesize() / 2
        TextSurf, TextRect = text_objects(text.split('\n')[0], font, colour)
        TextRect.center = (centX, centY - halfFontSize)
        surface.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects(text.split('\n')[1], font, colour)
        TextRect.center = (centX, centY + halfFontSize)
        surface.blit(TextSurf, TextRect)

    else:
        TextSurf, TextRect = text_objects(text, font, colour)
        TextRect.center = (centX, centY)
        surface.blit(TextSurf, TextRect)


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

##########################################################################
    # Angle Methods:
# 1) angle_Between:  #http://stackoverflow.com/a/31735642


def angle_between(point1, point2):  # http://stackoverflow.com/a/31735642
    #import numpy

    angle1 = math.atan2(*point1[::-1])  # investigate  # *x is power?
    angle2 = math.atan2(*point2[::-1])

    #angleRad = (angle1 - angle2) % (2 * math.pi)
    angleRad = (angle1 - angle2) % (2 * math.pi)

    # rand2deg converts radeon to degrees
    return math.degrees(angleRad)

# 2) Calculate angle between two vectors (Snipplr):
# http://snipplr.com/view/48794/calculate-angle-between-two-vectors/


def dotproduct(a, b):
    return sum([a[i] * b[i] for i in range(len(a))])


def veclength(a):
    # Calculates the size of a vector
    return sum([a[i] for i in range(len(a))])**.5


def clean_cos(cos_angle):
    return min(1, max(cos_angle, -1))


def ange(a, b):
    # Calculates the angle between two vector
    from math import acos

    dp = dotproduct(a, b)
    la = veclength(a)
    lb = veclength(b)
    costheta = dp / (la * lb)
    print "\ncostheta: ", costheta
    # is this even needed? can costheta ever get lower than -1?
    clean_cos(costheta)
    print "\nclean costheta: ", costheta, "\n"
    return acos(costheta)  # gives a math domain error if -1 <- costheta <= 1

# 3) determinant calculation clockwise angle:
# http://stackoverflow.com/a/31735880


def length(v):
    from math import sqrt

    return sqrt(v[0]**2 + v[1]**2)


def dot_product(v, w):
    return v[0] * w[0] + v[1] * w[1]


def determinant(v, w):
    return v[0] * w[1] - v[1] * w[0]


def inner_angle(v, w):
    from math import acos
    from math import pi

    cosx = dot_product(v, w) / (length(v) * length(w))
    rad = acos(cosx)  # in radians

    return rad * 180 / pi  # returns degrees


def angle_clockwise(A, B):
    inner = inner_angle(A, B)
    det = determinant(A, B)

    if det < 0:  # this is a property of the det. If the det < 0 then B is clockwise of A
        return inner
    else:  # if the det > 0 then A is immediately clockwise of B
        return 360 - inner

# 4) CMath angle:  # http://stackoverflow.com/a/31735605


def cmathAngle(a1, a2, b1, b2):
    import cmath

    a_phase = cmath.phase(complex(a1, a2))
    b_phase = cmath.phase(complex(b1, b2))
    angle = (a_phase - b_phase) * 180 / cmath.pi

    if angle < 0:
        angle += 360.0

    return angle

# 5) Theta Angle:  # http://stackoverflow.com/a/31735888


def thetaAngle(a, b):
    v1_theta = math.atan2(a[1], a[0])
    v2_theta = math.atan2(b[1], b[0])

    r = (v2_theta - v1_theta) * (180.0 / math.pi)

    if r < 0:
        r += 360.0

    return r


# 6) Simple Atan Vector Anlge:  #http://stackoverflow.com/a/42258870

def simpleAtan(centre, target):
    radiansAng = math.atan2(target[1] - centre[1], target[0] - centre[0])

    degreesAng = math.degrees(radiansAng)

    if degreesAng < 0:
        degreesAng = degreesAng + 360

    # 'rotates' the origin (or 0*) point to backwards 90*
    degreesAng = degreesAng + 90

    # accounts for previous calibration, so that any angle above 360 (ie,
    # north - origin point) is set to zero and upwards to 90
    if degreesAng >= 360:
        degreesAng = degreesAng - 360

    # This then, creates a clockwise angle readout from 0-359.99 in degrees

    return degreesAng
##########################################################################


while (True):
    for event in pygame.event.get():
        pass
    mouse = pygame.mouse.get_pos()   # needs to be re-defined every loop to update
    click = pygame.mouse.get_pressed()   # " "

    # print "mouse: ", mouse

    surface.fill(white)

    surface.blit(protractor_Img, (100, 0))

    if click[0] == 1:
        button_State = 1
    if button_State == 1 and click[0] == 0:
        button_State = 0
        prevMousePos = (mouse[0], mouse[1],)

    pygame.draw.rect(surface, red, (prevMousePos[0], prevMousePos[1], 5, 5))

    displayText("Curr mouse pos:\n%s, %s" % (str(mouse[0]), str(mouse[1])),
                smallText, black, 80, 30)
    displayText("Prev mouse pos:\n%s, %s" % (str(prevMousePos[0]), str(prevMousePos[1])),
                smallText, black, 80, 80)
    displayText("( prot centre: )\n%s" % (str(protCentre)),
                smallText, black, 80, 150)

    # Angle method calls:
    angle = angle_between(protCentre, mouse)
    displayText("Angle between:\n%s" % (str(angle)),
                smallText, black, canvas_width - 80, 30)

    if 0 not in mouse:  # avoids a zero division error
        detAngle = angle_clockwise(protCentre, mouse)
        displayText("Det Angle:\n%s" % (str(detAngle)),
                    smallText, black, canvas_width - 80, 80)
        """
        angleSnipplr = ange(protCentre, mouse)
        displayText("Angle (Snipplr):\n%s" % (str(angleSnipplr)),
                    smallText, black, canvas_width - 80, 60)
        """
        cAngle = cmathAngle(protCentre[0], protCentre[1], mouse[0], mouse[1])
        displayText("cMath Angle:\n%s" % (str(cAngle)),
                    smallText, black, canvas_width - 80, 130)

        thetAngle = thetaAngle(protCentre, mouse)
        displayText("Theta Angle:\n%s" % (str(thetAngle)),
                    smallText, black, canvas_width - 80, 190)

        # from testing, we see that this simplistic method most closely
        # resembles the data we are trying to get
        simpAtan = simpleAtan(protCentre, mouse)
        displayText("simpleAtan Angle:\n%s" % (str(simpAtan)),
                    smallText, black, canvas_width - 80, 250)

    pygame.draw.rect(surface, red, (0, protCentre[1], 1000, 2))
    pygame.draw.rect(surface, red, (protCentre[0], 0, 1, 1000))

    # limits surface update rate to a maximum of 60 frames per second
    # clock.tick(fps)
    # Pygame function to update surface with what has been blit-ed
    pygame.display.flip()
