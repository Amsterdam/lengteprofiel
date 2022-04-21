
import json
import os
from shapely.geometry import Point, LineString
import geopandas as gpd

from geotechnisch_lengteprofiel import Cptverzameling, Boreverzameling, GeotechnischLengteProfiel

profileName = 'test'

with open ("./profiel.geojson") as f:
    line = LineString(json.loads(f.read())["features"][0]["geometry"]["coordinates"])

cptPath = './cpts/'
borePath = './bores/'

fileList = os.listdir(cptPath)
fileList = [cptPath + f for f in fileList]
multicpt = Cptverzameling()
multicpt.load_multi_cpt(fileList)

fileList = os.listdir(borePath)
fileList = [borePath + f for f in fileList]
multibore = Boreverzameling()
multibore.load_multi_bore(fileList)

gtl = GeotechnischLengteProfiel()
gtl.set_line(line)
gtl.set_cpts(multicpt)
gtl.set_bores(multibore)
gtl.project_on_line()
gtl.set_groundlevel()
gtl.plot(boundaries={}, profilename=profileName)