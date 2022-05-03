
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


kades = ["DCG0102", "DCG0201", "DCG0202", "DCG0301", "DCG0302", "DCG0401", "DCG0402", "DCG0501", "DCG0502", "JLK0102", "DCG0102", "HGG0102", "HGG0103"] #"DCG0101", 
for kade in kades:
    print(kade)
    objectGDF = gpd.read_file("../../data/GIS/Kademuren/Kade Kunstwerk_20191007.geojson") # code loopt vast op de shp
    line = objectGDF[objectGDF['KUNSTWERKN'] == kade]['geometry'].iloc[0]
    boreList, cptList = readCptBores(f'../verzamel_grondonderzoek/omgenoemd/{kade}/')
    multicpt, multibore = make_multibore_multicpt(boreList, cptList)
    plotBoreCptInProfile(multicpt, multibore, line, kade)












def zakbakenToCsv():
    zbPath = './zakbaken/zakbaken.txt'
    zakbaken = pd.read_csv(zbPath, sep='\t', decimal=',')
    projectedLocations = []
    for i, zakbaak in zakbaken.iterrows():
        projectedLocations.append(line.project(Point(zakbaak['VoetPlaatX'], zakbaak['VoetPlaatY'])))
    zakbaken['afstand'] = projectedLocations
    zakbaken.to_csv('./output/afstandenZB.csv', sep=';', decimal=',')

def csvToProfile():
    path = './cpts/cpt.csv'
    cpts = pd.read_csv(path, sep=';', decimal=',')
    projectedLocations = []
    for i, cpt in cpts.iterrows():
        projectedLocations.append(line.project(Point(cpt['x'], cpt['y'])))
    cpts['afstand'] = projectedLocations
    cpts.to_csv('./output/afstandenExtraCpt.csv', sep=';', decimal=',')

def distanceOnLine(multicpt, multibore, line):
    gtl = GeotechnischLengteProfiel()
    gtl.set_line(line)
    gtl.set_cpts(multicpt)
    gtl.set_bores(multibore)
    gtl.project_on_line()
    gtl.set_groundlevel()
    return gtl

def writeToCsv(x, y, z, afstand, datum, testid, gtl):
    for cpt in gtl.cpts:
        x.append(cpt.easting)
        y.append(cpt.northing)
        z.append(cpt.groundlevel)
        afstand.append(cpt.projectedLocation * gtl.line.length)
        datum.append(cpt.date)
        testid.append(cpt.testid)

    df = pd.DataFrame()
    df['x'] = x
    df['y'] = y
    df['z'] = z
    df['afstand'] = afstand
    df['datum'] = datum 
    df['test'] = testid
    df.to_csv('./output/afstandenCPT.csv', sep=';', decimal=',')

def afstandenPuntenTotLijn():
    with open ("./profiel.geojson") as f:
        line = LineString(json.loads(f.read())["features"][0]["geometry"]["coordinates"])
    csvToProfile()
    x = []
    y = []
    z = []
    afstand = []
    datum = []
    testid = []

    multicpt, multibore = readCptBores()
    gtl = distanceOnLine(multicpt, multibore, line)
    writeToCsv(x, y, z, afstand, datum, testid, gtl)
    zakbakenToCsv()