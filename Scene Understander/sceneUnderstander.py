import json
import SULib
from pathlib import Path

# Reading json file into python dictionary. **
path = Path(__file__).with_name('cube.json') #
cfile = path.open('r')                       #
cfile = cfile.read()                         #
cube = json.loads(cfile)                     #

path = Path(__file__).with_name('one.json')  #
ofile = path.open('r')                       #
ofile = ofile.read()                         #
one = json.loads(ofile)                      #
#------------------------------------------ **


#Vertex Analysis for cube.json
SULib.vertexAnalysis(cube)