import geopandas as gpd
from plot_cpt_in_lengteprofiel import readCptBores, make_multibore_multicpt, plotBoreCptInProfile
import sys
sys.path.insert(0, '..\\cpt_viewer')
from gefxml_reader import Cpt, Bore

objectGDF = gpd.read_file("./input/profiel.geojson") # code loopt vast op de shp
line = objectGDF['geometry'].iloc[0]
boreList, cptList = readCptBores(f'./input/')
multicpt, multibore = make_multibore_multicpt(boreList, cptList)
plotBoreCptInProfile(multicpt, multibore, line, '')
