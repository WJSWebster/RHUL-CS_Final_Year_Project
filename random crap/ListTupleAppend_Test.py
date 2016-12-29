map_Coords = (20, 140)


mapFlags = [(15, 8), (15, 3), (6, 3), (6, 10), (13, 10), (13, 16), (5, 16)] # creates a list of tuples (cant be altered later) - this is only a temp variable.
#flagCoords = [(None, None)] * len(mapFlags)
#for idx in range(len(mapFlags)):
#for idx in xrange(1):
    #for ele in 2:
    #print "mapFlags[idx][0] = ", mapFlags[idx][0]
    #print "(' ' * 80) + map_Coords[0] = ", (((mapFlags[idx][0]) * 80) + map_Coords[0])
    #flagCoords.append((int((mapFlags[idx][0]) * 80) + map_Coords[0]), (int((mapFlags[idx][0]) * 80) + map_Coords[0]))
#print flagCoords


# in later implementations consider json.load(file) to load creep flag coords from txt file
mapFlags = [(15, 8), (15, 3), (6, 3), (6, 10), (13, 10), (13, 16), (5, 16)] # creates a list of tuples (cant be altered later) - this is only a temp variable

flagCoords = []
for mx, my in mapFlags:
    flagCoords.append(((mx * 80) + map_Coords[0], (my * 80) + map_Coords[1]))

print flagCoords
return flagCoords
