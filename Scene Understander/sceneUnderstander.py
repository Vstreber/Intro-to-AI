from SULib import vertexAnalysis, jsonToDictionary, regionLinking, globalBody

# Reading json file into python dictionary.
cube = jsonToDictionary('cube.json')
one = jsonToDictionary('one.json')
trial = jsonToDictionary('trial.json')


#================ CUBE.JSON ===================#

vertices = cube["vertex-data"]

cubeDict = dict()
ids = []
links = []
for vertex in vertices:
    v = dict()
    v["type"] = vertexAnalysis(vertex, cube)[0]
    v["notes"] = vertexAnalysis(vertex, cube)[1]
    v["links"] = regionLinking(vertex, cube, vertexAnalysis(vertex, cube)[1])
    links.append(regionLinking(vertex, cube, vertexAnalysis(vertex, cube)[1]))
    ids.append(dict(vertex)["id"])

    cubeDict.update({dict(vertex)["id"] : v})

print("+----------------------------------------------------------------------------------------------------+")
print("| ID  | TYPE  |           LINKS           |                          NOTES                           |")
print("|----------------------------------------------------------------------------------------------------|")
i=0
for id, v in cubeDict.items():
    print("| {:3} | {:5} | {:^25} | {:^56} | ".format(str(ids[i]),str(v["type"]), str(v["links"]), str(v["notes"])))
    i += 1
print("+----------------------------------------------------------------------------------------------------+")


globalBody(links)

#================ ONE.JSON ===================#

# vertices = one["vertex-data"]

# oneDict = dict()
# ids = []
# for vertex in vertices:
#     v = dict()
#     v["type"] = vertexAnalysis(vertex, one)[0]
#     v["notes"] = vertexAnalysis(vertex, one)[1]
#     v["links"] = regionLinking(vertex, one, vertexAnalysis(vertex, one)[1])
#     ids.append(dict(vertex)["id"])

#     oneDict.update({dict(vertex)["id"] : v})

# print("+----------------------------------------------------------------------------------------------------+")
# print("| ID  | TYPE  |           LINKS           |                          NOTES                           |")
# print("|----------------------------------------------------------------------------------------------------|")
# i=0
# for id, v in oneDict.items():
#     print("| {:3} | {:5} | {:^25} | {:^56} | ".format(str(ids[i]),str(v["type"]), str(v["links"]), str(v["notes"])))
#     i += 1
# print("+----------------------------------------------------------------------------------------------------+")

#================ TRIAL.JSON ===================#

# Vertex Analysis for 'trial.json'
# vertices = trial["vertex-data"]
# for vertex in vertices:
#     id = dict(vertex)["id"]
#     print(id, ": ", vertexAnalysis(vertex, trial)[0])