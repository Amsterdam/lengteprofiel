
import json
import os
from shapely.geometry import Point, LineString
import pandas as pd
import geopandas as gpd
import sys

from geotechnisch_lengteprofiel import Cptverzameling, Boreverzameling, GeotechnischLengteProfiel
sys.path.insert(0, '..\\cpt_viewer')
from gefxml_reader import Cpt, Bore, Test

def readCptBores(path):

    files = os.listdir(path)
    files = [path + f for f in files]
    cptList = []
    boreList = []

    for f in files:
        if f.lower().endswith('gef'):
            testType = Test().load_gef(f)
            if testType == 'cpt':
                cptList.append(f)
            elif testType == 'bore':
                boreList.append(f)
        elif f.lower().endswith('xml'):
            testType = Test().load_xml(f)
            if testType == 'cpt':
                cptList.append(f)
            elif testType == 'bore':
                boreList.append(f)
    
    return boreList, cptList

def make_multibore_multicpt(boreList, cptList):
    multicpt = Cptverzameling()
    multicpt.load_multi_cpt(cptList)
    multibore = Boreverzameling()
    multibore.load_multi_bore(boreList)
    return multicpt, multibore

def plotBoreCptInProfile(multicpt, multibore, line, profileName):
    gtl = GeotechnischLengteProfiel()
    gtl.set_line(line)
    gtl.set_cpts(multicpt)
    gtl.set_bores(multibore)
    gtl.project_on_line()
    gtl.set_groundlevel()
    gtl.plot(boundaries={}, profilename=profileName)


kades = ["DCG0101", "DCG0102", "DCG0201", "DCG0202", "DCG0301", "DCG0302", "DCG0401", "DCG0402", "DCG0501", "DCG0502", "JLK0102", "HGG0102", "HGG0103"] 
kades = ["KBW0202"]
for kade in kades:
    print(kade)
    objectGDF = gpd.read_file("../../data/GIS/Kademuren/Kade Kunstwerk_20191007.geojson") # code loopt vast op de shp
    line = objectGDF[objectGDF['KUNSTWERKN'] == kade]['geometry'].iloc[0]
    boreList, cptList = readCptBores(f'../verzamel_grondonderzoek/omgenoemd/{kade}/')
    multicpt, multibore = make_multibore_multicpt(boreList, cptList)
    plotBoreCptInProfile(multicpt, multibore, line, kade)