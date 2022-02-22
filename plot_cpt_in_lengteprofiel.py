
import json
import os
from shapely.geometry import Point, LineString
import geopandas as gpd

from geotechnisch_lengteprofiel import Cptverzameling, Boreverzameling, GeotechnischLengteProfiel

kades = ["DCK-water"]
kades = ["HGG0103", "DCG0101", "DCG0201", "DCG0202", "DCG0301", "DCG0302", "DCG0401", "DCG0402", "DCG0501", "DCG0502", "JLK0102"] #DCK
geodf = gpd.read_file("../PBK/webkaart/Bruggen_en_kades/Kade Kunstwerk_20191007.geojson")

for kade in kades:
    print(kade)
    if kade == "DCK-water":
        line = LineString([(119987, 487343), (119910, 487129), (119940, 486950), (120098, 486581)])
    else:
        line = geodf[geodf["KUNSTWERKN"] == kade].geometry.iloc[0]

    cptPath = f"C:/Users/User/scripts/PBK/webkaart/omgenoemd/{kade}/"

    fileList = os.listdir(cptPath)
    fileList = [cptPath + f for f in fileList]
    multicpt = Cptverzameling()
    multicpt.load_multi_cpt(fileList)

    multibore = Boreverzameling()

    gtl = GeotechnischLengteProfiel()
    gtl.set_line(line)
    gtl.set_cpts(multicpt)
    gtl.set_bores(multibore)
    gtl.project_on_line()
    gtl.set_groundlevel()
    gtl.plot(boundaries={}, filename=kade)