import math

a = [70, 24]
b = [140, 0]

angle = math.atan2(a[1], a[0]) - math.atan2(b[1], b[0])
angle = angle * 360 / (2 * math.pi)

if angle < 0:
	angle = angle + 360

print "angle: ", angle
