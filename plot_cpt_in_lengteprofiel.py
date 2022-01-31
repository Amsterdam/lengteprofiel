
import json
import os
from shapely.geometry import Point, LineString
import geopandas as gpd

from geotechnisch_lengteprofiel import Cptverzameling, Boreverzameling, GeotechnischLengteProfiel

line = gpd.read_file('D:/Profiellijn.shp')["geometry"][0]

cptPath = "C:/Users/User/scripts/PBK/webkaart/omgenoemd/IJtram_A-E/"

fileList = os.listdir(cptPath)
fileList = [cptPath + f for f in fileList]
multicpt = Cptverzameling()
multicpt.load_multi_cpt(fileList)

fileList = os.listdir(f"{cptPath}boringen/")
fileList = ["./bores/" + f for f in fileList]
multibore = Boreverzameling()
multibore.load_multi_bore(fileList)

gtl = GeotechnischLengteProfiel()
gtl.set_line(line)
gtl.set_cpts(multicpt)
gtl.set_bores(multibore)
gtl.project_on_line()
gtl.set_groundlevel()
gtl.plot(boundaries={})