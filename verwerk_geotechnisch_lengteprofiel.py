
import json
import os
from shapely.geometry import Point, LineString


from geotechnisch_lengteprofiel import Cptverzameling, Boreverzameling, GeotechnischLengteProfiel

profileName = 'test'

with open ("./profiel.geojson") as f:
    line = LineString(json.loads(f.read())["features"][0]["geometry"]["coordinates"])

cptPath = "./cpts/"

fileList = os.listdir(cptPath)
fileList = [cptPath + f for f in fileList]
multicpt = Cptverzameling()
multicpt.load_multi_cpt(fileList)

fileList = os.listdir("./bores/")
fileList = ["./bores/" + f for f in fileList]
multibore = Boreverzameling()
multibore.load_multi_bore(fileList)

gtl = GeotechnischLengteProfiel()
gtl.set_line(line)
gtl.set_cpts(multicpt)
gtl.set_bores(multibore)
gtl.project_on_line()
gtl.set_groundlevel()
gtl.set_profilename(profileName)
gtl.set_layers("./layers.xlsx")

# instellen van variabelen
gtl.canvasWidth = 1800 # breedte van canvas
gtl.canvasHeight = 750 # hoogte van canvas
gtl.xScaleCPT = 5 # horizontale schaal voor lijnen van cpt op canvas

gtl.create_canvas_with_cpts()

# TODO: voeg meer toe aan self?
# TODO: maak dat je ook zonder boundaries kan plotten, dus alleen het ruwe grondonderzoek