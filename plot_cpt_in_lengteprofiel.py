import os
import geopandas as gpd
import sys

from geotechnisch_lengteprofiel import Cptverzameling, Boreverzameling, GeotechnischLengteProfiel
sys.path.insert(0, '../gefxml_viewer')
from gefxml_reader import Cpt, Bore, Test

def readCptBores(path):

    files = os.listdir(path)
    files = [path + f for f in files]
    cptList = []
    boreList = []
    sikbFileList = []

    for f in files:
        if f.lower().endswith('gef'):
            testType = Test().type_from_gef(f)
            if testType == 'cpt':
                cptList.append(f)
            elif testType == 'bore':
                boreList.append(f)
        elif f.lower().endswith('xml'):
            testType = Test().type_from_xml(f)
            if testType == 'cpt':
                cptList.append(f)
            elif testType == 'bore':
                boreList.append(f)
        elif f.lower().endswith('csv'):
            sikbFileList.append(f)

    return boreList, cptList, sikbFileList

def make_multibore_multicpt(boreList, cptList, sikbFileList):
    multicpt = Cptverzameling()
    multicpt.load_multi_cpt(cptList)
    multibore = Boreverzameling()
    multibore.load_multi_bore(boreList)
    multibore.load_sikb(sikbFileList)
    return multicpt, multibore

def plotBoreCptInProfile(multicpt, multibore, line, profileName):
    gtl = GeotechnischLengteProfiel()
    gtl.set_line(line)
    gtl.set_cpts(multicpt)
    gtl.set_bores(multibore)
    gtl.project_on_line()
    gtl.set_groundlevel()
    gtl.plot(boundaries={}, profilename=profileName)

if __name__ == "__main__":
    objectGDF = gpd.read_file(f"./input/profiel.geojson")
    line = objectGDF['geometry'].iloc[0]

    boreList, cptList, sikbFileList = readCptBores(f'./input/')
    multicpt, multibore = make_multibore_multicpt(boreList, cptList, sikbFileList)
    plotBoreCptInProfile(multicpt, multibore, line, profileName="")