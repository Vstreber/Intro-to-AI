import json, math
import collections.abc
from pathlib import Path

def jsonToDictionary(filename):
    path = Path(__file__).with_name(filename)
    cfile = path.open('r')                    
    cfile = cfile.read()                         
    dictionary = json.loads(cfile)
    return dictionary

def vertexAnalysis(vertex,image):
    try:
        return vertexAnalysis1(vertex, image)
    except:
        return vertexAnalysis2(vertex, image)

def vertexAnalysis1(vertex, image):
    
    #Getting dictionary for calculating angles later.
    vertices = image["vertex-data"]

    #Defining input vertex attributes.
    coords = dict(vertex)["coords"]
    kind = dict(vertex)["kind-list"]
    kindVertexOnly = []

    #Extracting points from kind list, ignoring surfaces and repeats.
    for x in kind:
        if (isinstance(x, str)) & (x not in kindVertexOnly):
            kindVertexOnly.append(x)

    #Checking for "L"
    if len(kindVertexOnly) == 2:
        return ["L", "No notes"]

    #Checking for "Fork", "Arrow", and "T"
    if len(kindVertexOnly) >= 3:

        P1 = [d['coords'] for d in vertices if d['id'] == kindVertexOnly[0]][0]
        P2 = [d['coords'] for d in vertices if d['id'] == kindVertexOnly[1]][0]
        P3 = [d['coords'] for d in vertices if d['id'] == kindVertexOnly[2]][0]

        angle1 = getAngle(P1,coords,P2)
        angle2 = getAngle(P3,coords,P1)
        angle3 = getAngle(P2,coords,P3)

        #If angles aren't calculated correctly by this function, raises exception that switches to the reverse function.
        if (angle1 > 180 and angle2 > 180) or (angle2 > 180 and angle3 > 180) or (angle1 > 180 and angle3 > 180):
            raise Exception("Invalid angle combination - more than two are over 180 degrees.")

        #checking for "T"
        if (isInRange(angle1,180,5)) or (isInRange(angle2,180,5)) or (isInRange(angle3,180,5)):
            return ["T", "No notes"]
        
        #checking for "Fork"
        if (angle1 < 180) and (angle2 < 180) and (angle3 < 180):
            return ["Fork", "No notes"]
        
        #checking for "Arrow"
        if (angle1 > 180) or (angle2 > 180) or (angle3 > 180):
            twoSmallest = [];
            for angle in [angle1,angle2,angle3]:
                if angle != max([angle1,angle2,angle3]):
                    if angle == angle1:
                        twoSmallest.append([kindVertexOnly[0], [kindVertexOnly[1]]])
                    if angle == angle2:
                        twoSmallest.append([kindVertexOnly[2], [kindVertexOnly[0]]])
                    if angle == angle3:
                        twoSmallest.append([kindVertexOnly[1], [kindVertexOnly[2]]])
            return ["Arrow", twoSmallest]


def vertexAnalysis2(vertex, image):
    
    #Getting dictionary for calculating angles later.
    vertices = image["vertex-data"]

    #Defining input vertex attributes.
    coords = dict(vertex)["coords"]
    kind = dict(vertex)["kind-list"]
    kindVertexOnly = []

    #Extracting points from kind list, ignoring surfaces and repeats.
    for x in kind:
        if (isinstance(x, str)) & (x not in kindVertexOnly):
            kindVertexOnly.append(x)

    #Checking for "L"
    if len(kindVertexOnly) == 2:
        return ["L", "No notes"]

    #Checking for "Fork", "Arrow", and "T"
    if len(kindVertexOnly) >= 3:

        P1 = [d['coords'] for d in vertices if d['id'] == kindVertexOnly[0]][0]
        P2 = [d['coords'] for d in vertices if d['id'] == kindVertexOnly[1]][0]
        P3 = [d['coords'] for d in vertices if d['id'] == kindVertexOnly[2]][0]

        angle3 = getAngle(P2,coords,P1)
        angle2 = getAngle(P1,coords,P3)
        angle1 = getAngle(P3,coords,P2)

        #checking for "T"
        if (isInRange(angle1,180,5)) or (isInRange(angle2,180,5)) or (isInRange(angle3,180,5)):
            return ["T", "No notes"]
        
        #checking for "Fork"
        if (angle1 < 180) and (angle2 < 180) and (angle3 < 180):
            return ["Fork", "No notes"]
        
        #checking for "Arrow"
        if (angle1 > 180) or (angle2 > 180) or (angle3 > 180):
            twoSmallest = [];
            for angle in [angle1,angle2,angle3]:
                if angle != max([angle1,angle2,angle3]):
                    if angle == angle1:
                        twoSmallest.append([kindVertexOnly[1], [kindVertexOnly[2]]])
                    elif angle == angle2:
                        twoSmallest.append([kindVertexOnly[0], [kindVertexOnly[2]]])
                    elif angle == angle3:
                        twoSmallest.append([kindVertexOnly[1], [kindVertexOnly[0]]])
            return ["Arrow", twoSmallest]      

def getAngle(a, b, c):
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    if ang < 0:
        ang += 360
    
    return ang

def isInRange(value1, value2, maxCloseness):
    return abs(value1 - value2) <= maxCloseness

def regionLinking(vertex, image, twoSmallest):
    links = []
    #Extracting surfaces from kind list, ignoring points.
    kind = dict(vertex)["kind-list"]
    
    bg = image["background"]

    #Links for "L, T"
    if (vertexAnalysis(vertex, image)[0] == "L") or (vertexAnalysis(vertex, image)[0] == "T"):
        # No links generated
        return None
    
    #Links for "Arrow"
    if vertexAnalysis(vertex, image)[0] == "Arrow":
        for i in range(len(kind)):
            if (isinstance(kind[i], int)):
                if (kind[i-1] == twoSmallest[0][0]) and (kind[i+1] == twoSmallest[0][1][0]):
                    links.append(kind[i])
                elif (kind[i-1] == twoSmallest[1][0]) and (kind[i+1] == twoSmallest[1][1][0]):
                    links.append(kind[i])
        return links

    #Links for "Fork"
    if vertexAnalysis(vertex, image)[0] == "Fork":
        surfaces = []
        for i in range(len(kind)):
            if (isinstance(kind[i], int)) and (kind[i] != bg):
                surfaces.append(kind[i])

        links.append([surfaces[0],surfaces[1]])
        links.append([surfaces[0],surfaces[2]])
        links.append([surfaces[1],surfaces[2]])
        return links
    
def globalBody(links):
    cleanedLinks = []
    for link in links:
        if link != None:
            if isinstance(link[0], collections.abc.Sequence):
                link[0].sort()
                link[1].sort()
                link[2].sort()
                cleanedLinks.append(link[0])
                cleanedLinks.append(link[1])
                cleanedLinks.append(link[2])
            else:
                link.sort()
                cleanedLinks.append(link)
    linkOccurences = dict()

    surfaces = []

    for link in cleanedLinks:
        linkOccurences.update({str(link) : 0})
        surfaces.append(link[0])
        surfaces.append(link[1])

    surfaces = list(set(surfaces))

    for link in cleanedLinks:
        num = linkOccurences[str(link)]
        num += 1
        linkOccurences.update({str(link) : num})

    print(linkOccurences)
    print(surfaces)

    nuclei = []
    for i in surfaces:
        nuclei.append([i])

    for x in range(2): #goes until nuclei is only length of 1
        newNuclei = []
        for l in linkOccurences:
            if linkOccurences[l] >=2:
                for n in nuclei:
                    if n == l[0]: 
                        newNuclei + n
                        nuclei.pop(n)
                    if n == l[1]:
                        newNuclei + n
                        nuclei.pop(n)
                    if len(n) > 1:
                        if l[0] in n:
                            nuclei + l[0]
                        if l[1] in n:
                            nuclei + l[0]
                nuclei.append(newNuclei)
                print(nuclei)