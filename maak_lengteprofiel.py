import geopandas as gpd
from plot_cpt_in_lengteprofiel import readCptBores, make_multibore_multicpt, plotBoreCptInProfile

objectGDF = gpd.read_file(f"./input/profiel.geojson")
line = objectGDF['geometry'].iloc[0]

boreList, cptList, sikbFileList = readCptBores(f'./input/')
multicpt, multibore = make_multibore_multicpt(boreList, cptList, sikbFileList)
plotBoreCptInProfile(multicpt, multibore, line, profileName="")