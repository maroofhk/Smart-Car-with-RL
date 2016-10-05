lst = [(100, 0), (100, 100), (100, 200), (100, 300), (200, 300), (300, 300), (300, 400), (300, 500), (300, 600), (400, 600), (500, 600), (600, 600)]
angle = [270, 270, 0, 0, 270, 270, 0, 0, 0]

def expandPath(gamePath):
    expandedPath = []
    count = 0
    while count < len(gamePath)-1:
        currentGridCoord = gamePath[count]
        expandedPath.append(currentGridCoord)
        
        delta_x = int((gamePath[count+1][0] - gamePath[count][0])/10)
        delta_y = int((gamePath[count+1][1] - gamePath[count][1])/10)

        x, y = currentGridCoord
        for _ in range(9):
            
            x = x + delta_x
            y = y + delta_y
            print(x,y)
            expandedPath.append( (x, y)  )
            
        count += 1
    expandedPath.append(gamePath[-1])
    
    return expandedPath

def expandAngle(angleList):
    expandedAngle = []
    count = 0
    while count < len(angleList)-1:
        currentAngle = angleList[count]
        expandedAngle.append(currentAngle)

        angle = currentAngle
    
        delta = int((angleList[count+1] - angleList[count])/10)
        for _ in range(9):
            angle = angle + delta
            print(angle)
            expandedAngle.append(angle)
        print('count: ', count)
        count += 1
    expandedAngle.append(angleList[-1])

    return expandedAngle

def expandAngle2(angleList):
    expandedAngle = []
    count = 0
    while count < len(angleList)-1:
        currentAngle = angleList[count]
        expandedAngle.append(currentAngle)

        angle = currentAngle

        first = angleList[count]
        last = angleList[count + 1]
        avg = 0.5*(first + last)
        extra = []
        expandedAngle.extend(extra)
    
##        delta = int((angleList[count+1] - angleList[count])/10)
##        for _ in range(9):
##            angle = angle + delta
##            print(angle)
##            expandedAngle.append(angle)
##        print('count: ', count)
        count += 1
    expandedAngle.append(angleList[-1])

    return expandedAngle

#print('original list: ', lst)

#expandPath(lst)
#print('expanded list: ', expandPath(lst))
print('starting angle', len(angle))
print('expanded angle: ', expandAngle2(angle))
