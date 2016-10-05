from math import floor, ceil

def getGridCoord(x,y):
	outX = 0
	outY = 0

	if  x % 100 < 50:
		outX = floor(x / 100)
	else: 
		outX = ceil(x / 100)

	if y % 100 < 50:
		outY = floor(y / 100)
	else:
		outY = ceil(y / 100)

	return outY, outX

out = getGridCoord(340,460)
print(out)