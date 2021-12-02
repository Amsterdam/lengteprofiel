"""
Script om geotechnische lengteprofielen te tekenen
Geschreven door Thomas van der Linden, Ingenieursbureau Amsterdam
19 oktober 2021

Input:
- sonderingen, als XML of GEF in een map met de naam cpts in dezelfde directory als de code
- profiellijn, als geojson bestand
- lagen, als excel tabel met de naam layers.xlsx in dezelfde directory als de code
    de tabel heeft kolommen laag (nummer in dezelfde volgorde als je getekend hebt), materiaal, plotkleur (in het Engels)

Output:
- output.geo dat ingelezen kan worden in de D-Serie # TODO: materialen toevoegen
- gtl.png en gtl.svg figuren met het geotechnisch lengteprofiel

Het programma opent een venster waarin geklikt kan worden om lijnen op te geven
Een klik met de linker muisknop voegt een punt toe aan de lijn (grens)
Een klik met de rechter muisknop creëert een nieuwe lijn (grens)
Sluit het venster af met de knop Quit, anders blijft het programma lopen en wordt er geen output gemaakt

Afhankelijkheden
- cpt_reader geschreven door Thomas van der Linden 
- standaard Python packages
"""


# TODO: ordenen, methods onderbrengen in classes
# TODO: kan het ook runnen zonder eerst een canvas, maar direct een plaatje


import numpy as np
import pandas as pd
from shapely.geometry import Point, LineString
import os
import sys
import json
import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt

sys.path.insert(0, '..\\cpt_viewer')
from cpt_reader import Cpt, Bore

line = LineString([(120097, 487385), (119981, 487339), (119935, 487200), (119908, 487040), (120099, 486579)]) # Deze moet je zelf opgeven

with open ("./profiel.geojson") as f:
    line = LineString(json.loads(f.read())["features"][0]["geometry"]["coordinates"])

class Cptverzameling():
    def __init__(self):
        self.cpts = []

    def load_multi_cpt(self, fileList):
        for f in fileList:
            cpt = Cpt()
            if f.lower().endswith("xml"):
                cpt.load_xml(f)
                self.cpts.append(cpt)
            elif f.lower().endswith("gef"):
                cpt.load_gef(f)
                self.cpts.append(cpt)

class Boreverzameling():
    def __init__(self):
        self.bores = []
    
    def load_multi_bore(self, fileList):
        for f in fileList:
            bore = Bore()
            if f.lower().endswith("xml"):
                bore.load_xml(f)
                self.bores.append(bore)

class GeotechnischLengteProfiel():
    def __init__(self):
        self.line = None
        self.cpts = None
        self.materials = None
        self.boundaries = {}
        self.groundlevelRel = []
        self.groundlevelAbs = []

    def set_line(self, line):
        self.line = line

    def set_cpts(self, cptVerzameling):
        self.cpts = cptVerzameling.cpts

    def set_bores(self, boreVerzameling):
        self.bores = boreVerzameling.bores

    def set_layers(self, materialsTable):
        materials = pd.read_excel(materialsTable, index_col="laag")
        self.materials = materials
     
    def project_on_line(self):
        for cpt in self.cpts:
            cptLocation = Point(cpt.easting, cpt.northing)
            cpt.projectedLocation = self.line.project(cptLocation, normalized=True)
        for bore in self.bores:
            boreLocation = Point(bore.easting, bore.northing)
            bore.projectedLocation = self.line.project(boreLocation, normalized=True)

    def set_groundlevel(self):
        # TODO: dit is niet zo mooi

        for bore in self.bores:
            self.groundlevelRel.append([bore.projectedLocation, bore.groundlevel])
            self.groundlevelAbs.append([bore.projectedLocation * self.line.length, bore.groundlevel])
        for cpt in self.cpts:
            self.groundlevelRel.append([cpt.projectedLocation, cpt.groundlevel])
            self.groundlevelAbs.append([cpt.projectedLocation * self.line.length, cpt.groundlevel])

        self.groundlevelAbs.sort()
        self.groundlevelAbs.insert(0, [0, self.groundlevelAbs[0][1]])
        self.groundlevelAbs.append([self.line.length, self.groundlevelAbs[-1][1]])
        self.groundlevelAbs = np.asarray(self.groundlevelAbs)

        self.groundlevelRel.sort()
        self.groundlevelRel.insert(0, [0, self.groundlevelRel[0][1]])
        self.groundlevelRel.append([self.line.length, self.groundlevelRel[-1][1]])
        self.groundlevelRel = np.asarray(self.groundlevelRel)

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
gtl.set_layers("./layers.xlsx")

def plot(gtl, boundaries):
    fig, ax1 = plt.subplots(figsize=(30, 7))

    # plot de cpts
    for cpt in gtl.cpts:
        qcX = cpt.data["coneResistance"] / 2 + cpt.projectedLocation * gtl.line.length # TODO: ipv een vaste waarde een factor afhankelijk van aantal cpts en tussenafstand?
        rfX = cpt.data["frictionRatio"] / 2 + cpt.projectedLocation * gtl.line.length # TODO: ipv vaste waarde een factor afhankelijk van aantal cpts en tussenafstand?
        y = -1 * cpt.data["depth"] + cpt.groundlevel
        plt.plot(qcX, y, c="blue", linewidth=0.5)
        plt.plot(rfX, y, c="green", linewidth=0.5)
        plt.text(qcX.min(), y.max(), cpt.testid)
        plt.grid(b=True)
        plt.minorticks_on()
        plt.grid(b=True, which="minor", lw=0.1)

    # plot de boringen
    for bore in gtl.bores:
        boreX = bore.projectedLocation * gtl.line.length
        for i, layer in bore.soillayers.iterrows():
            plt.plot([boreX, boreX], [layer.upper_NAP, layer.lower_NAP], layer.plotColor)

    # plot de laaggrenzen als lijnen
    for boundary, points in boundaries.items():
        points = np.array(points)
        plt.plot(points[:,0], points[:,1], c="black")

    # kleur de lagen
    for boundary in boundaries.keys():
        if boundary < max(boundaries.keys()):
            pointsTop = np.array(boundaries[boundary + 1])
            pointsBottom = np.array(boundaries[boundary])

            xTop = pointsTop[:,0]
            yTop = pointsTop[:,1]
            xBottom = pointsBottom[:,0]
            yBottom = pointsBottom[:,1]

            # zorgen dat beide lijnen dezelfde x-coördinaten hebben
            allX = np.concatenate((xTop, xBottom))
            allX = np.unique(allX)
            allX = np.sort(allX)
            
            # y waarden interpoleren
            allYTop = np.interp(allX, xTop, yTop)
            allYBottom = np.interp(allX, xBottom, yBottom)            

            plt.fill_between(allX, allYBottom, allYTop, color=gtl.materials.loc[boundary]["kleur"])
            
    ax2 = ax1.twinx().set_ylim(ax1.get_ylim())
    
    ax1.set_xlabel("afstand [m]")
    ax1.set_ylabel("niveau [m t.o.v. NAP]")

    plt.savefig("./gtl.svg", bbox_inches="tight")
    plt.savefig("./gtl.png", bbox_inches="tight")   

def add_line(eventorigin):
    # deze functie maakt het mogelijk om een lijn (grens) toe te voegen 
    global i
    i += 1 # TODO: dit zou toch via gtl.boundaries moeten kunnen?

tklines = []
def draw_line(eventorigin):
    # deze functie maakt het mogelijk om een lijn (grens) te tekenen
    global tkline
    global x,y
    x = eventorigin.x
    y = eventorigin.y
    
    # check of er een nieuwe lijn is begonnen
    # dan deze toevoegen aan de verzameling
    if i not in gtl.boundaries.keys():
        # voeg het geklikte punt toe aan de lijn
        gtl.boundaries[i] = [[x,y]]
    else:
        # voeg het geklikte punt toe aan de lijn
        gtl.boundaries[i].append([x,y])
    # teken de lijn (als er meer dan 1 punt is)
    if len(gtl.boundaries[i]) > 1:
        tkline = C.create_line(gtl.boundaries[i])
        tklines.append(tkline)

def remove_last_point(eventorigin):
    # deze functie verwijdert het laatste punt van de laatste boundary (kan meerdere punten verwijderen)
    # en verwijdert het laatst getekende lijnstuk
    last_boundary = max(gtl.boundaries.keys())
    if len(gtl.boundaries[last_boundary]) > 0:
        del gtl.boundaries[last_boundary][-1]
        C.delete(tklines[-1])
        del tklines[-1]

def finish():
    # deze functie zorgt voor het afsluiten van het tekenvenster 
    # en het verder verwerken van de ingevoerde punten / grenzen
    root.quit()

    # verwijder het laatste punt van boundaries, dat ontstaat bij het sluiten
    gtl.boundaries[max(gtl.boundaries.keys())] = gtl.boundaries[max(gtl.boundaries.keys())][:-1]
    
    yScale, top = get_yscale_for_canvas(gtl.cpts, gtl.bores, canvasHeight)
    realLength = line.length
    scaledBoundaries = scale_points_to_real_world(gtl.boundaries, realLength, canvasWidth, yScale, top)
    boundariesModifiedLimits = modify_geometry_limits(scaledBoundaries, 0, realLength)
    
    # voeg het maaiveld toe
    boundariesModifiedLimits[1] = gtl.groundlevelAbs.tolist()

    # TODO: eigenlijk moeten de gtl.boundaries worden vervangen door de boundariesModifiedLimits 
    
    write_to_DSerie_input(boundariesModifiedLimits)
    plot(gtl, boundariesModifiedLimits)

def write_to_DSerie_input(boundaries):
    # deze functie maakt een geometriebestand dat ingelezen kan worden in de D-Serie
    pointsi = 1
    pointstxt = ""

    for points in boundaries.values():
        for point in points:
            pointstxt += f'\t\t{pointsi}\t{round(point[0], 3)}\t\t{round(point[1], 3)}\t\t0.000\n'
            pointsi += 1
    pointstxt = f"[POINTS]\n\t{pointsi - 1} - Number of geometry points -\n" + pointstxt
    pointstxt += "[END OF POINTS]\n"
        
    pointsi = 2
    curvesi = 1
    curvestxt = ""
    boundstxt = ""

    maxBoundary = max(boundaries.keys())
    for boundary, points in boundaries.items():
        startcurve = curvesi
        for point in range(len(points)-1):
            curvestxt += f"\t{curvesi} - Curve number\n"
            curvestxt += f"\t\t2 - number of points on curve, next line(s) are pointnumbers\n"
            curvestxt += f"\t\t\t{pointsi-1}\t{pointsi}\n"
            pointsi += 1
            curvesi += 1
        endcurve = curvesi
        pointsi += 1

        boundtxt = f"\t{maxBoundary - boundary} - Boundary number\n"
        boundtxt += f"\t\t{endcurve - startcurve} - number of curves on boundary, next line(s) are curvenumbers\n\t\t\t"
        for curve in range(startcurve, endcurve):
            boundtxt += f"{curve}\t"
        boundtxt += "\n"

        boundstxt = boundtxt + boundstxt

    curvestxt = f"[CURVES]\n\t{curvesi - 1}\t- Number of curves -\n" + curvestxt
    curvestxt += "[END OF CURVES]\n"
    
    boundstxt = f"[BOUNDARIES]\n\t{len(boundaries.keys())}\t- Number of boundaries -\n" + boundstxt
    boundstxt += "[END OF BOUNDARIES]\n"
    
    layerstxt = f"[LAYERS]\n" 
    layerstxt += f"{len(boundaries.keys()) - 1} - Number of Layers -\n"
    for boundaryi in range(len(boundaries.keys())-1):
        layerstxt += f"\t{boundaryi + 1} - Layer number, next line is material of layer\n"
        layerstxt += f"\t\tmaterial\n"
        layerstxt += f"\t\t0 - Piezometric level line at top of layer\n"
        layerstxt += f"\t\t0 - Piezometric level line at bottom of layer\n"
        layerstxt += f"\t\t{boundaryi + 1} - Boundarynumber at top of layer\n"
        layerstxt += f"\t\t{boundaryi} - Boundarynumber at bottom of layer\n"
    layerstxt += "[END OF LAYERS]\n"

    headertxt = "GEOMETRY FILE FOR THE M-SERIES\n"
    headertxt += "==============================================================================\n"
    headertxt += "COMPANY    : Gemeente Amsterdam Ingenieursbureau  \n"
    headertxt += f"DATE       : {datetime.today().strftime('%m/%d/%Y')}\n"
    headertxt += f"TIME       : {datetime.now().strftime('%I:%M:%S %p')}\n"
    headertxt += "FILENAME   : H:/test.geo\n"
    headertxt += "CREATED BY : D-Settlement version 20.1.1.29740\n"
    headertxt += "==========================    BEGINNING OF DATA     ==========================\n"
    headertxt += "[TITLES]\n"
    headertxt += "Geometry created with a tool written by Thomas van der Linden\n"
    headertxt += "\n"
    headertxt += "[END OF TITLES]\n"
    headertxt += "[EXTRA TITLE]\n"
    headertxt += "\n"
    headertxt += "[END OF EXTRA TITLE]\n"
    headertxt += "[ACCURACY]\n"
    headertxt += "\t0.0010\n"
    headertxt += "[END OF ACCURACY]\n"
    headertxt += "\n"

    with open("./output.geo", "w") as output:
        output.write(headertxt)
        output.write(pointstxt)
        output.write(curvestxt)
        output.write(boundstxt)
        output.write(layerstxt)
        output.write("END OF GEOMETRY FILE")

def modify_geometry_limits(boundaries, leftLimit, rightLimit):
    # deze functie zorgt ervoor dat alle eerste punten op een grens x=0 hebben
    # en alle laatste punten op een grens x=lengte van de lijn
    
    for boundary, points in boundaries.items():
        points.insert(0, [leftLimit, points[0][1]])
        points.append([rightLimit, points[-1][1]])
    return boundaries

def scale_points_to_real_world(boundaries, realLength, canvasWidth, yScale, top):
    # deze functie schaalt de coördinaten van het canvas naar de fysieke wereld
    scaledBoundaries = {}
    for boundary, points in boundaries.items():
        points = np.array(points)
        scaledX = points[:,0] * realLength / canvasWidth
        scaledY = top - 1 * points[:,1] / yScale
        scaledBoundaries[boundary] = [[scaledX, scaledY] for scaledX, scaledY in list(zip(scaledX, scaledY))]
    return scaledBoundaries

def get_yscale_for_canvas(cpts, bores, canvasHeight):
    # volgende blok bepaalt de yscale
    groundlevels = []
    finaldepths = []
    for cpt in cpts:
        groundlevels.append(cpt.groundlevel)
        finaldepths.append(cpt.finaldepth)
    for bore in bores:
        groundlevels.append(bore.groundlevel)
        finaldepths.append(bore.finaldepth) 
    top = max(groundlevels)
    length = max(finaldepths)
    yscale = canvasHeight / length

    return yscale, top

def scale_cpt_to_canvas(cpt, xScaleCPT, yscale, groundlevel, top, width):
    qcX = cpt.data["coneResistance"] * xScaleCPT + cpt.projectedLocation * width # uses relative projectedLocation (0-1)
    rfX = cpt.data["frictionRatio"]  * xScaleCPT + cpt.projectedLocation * width # uses relative projectedLocation (0-1)
    y = (top - groundlevel + cpt.data["depth"]) * yscale 
    return qcX, rfX, y

def scale_bore_to_canvas(bore, yscale, groundlevel, top, width):
    xs = np.full(len(bore.soillayers.index), bore.projectedLocation * width)
    uppers = (top - groundlevel + bore.soillayers["upper"]) * yscale 
    lowers = (top - groundlevel + bore.soillayers["lower"]) * yscale 
    return xs, uppers, lowers

def scale_groundlevel_to_canvas(gtl, yscale, top, width):
    xs = gtl.groundlevelRel[:,0] * width
    ys = (gtl.groundlevelRel[:,1] * -1 + top) * yscale
    return xs, ys

def create_canvas_with_cpts(gtl, canvasWidth, canvasHeight, xScaleCPT):
    # deze functie maakt een canvas met daarop plots van cpts

    # maak het canvas
    global C, i, root
    root = tk.Tk()
    C = tk.Canvas(root, height=canvasHeight, width=canvasWidth)

    # bepaal de schaal voor de verticale as
    yscale, top = get_yscale_for_canvas(gtl.cpts, gtl.bores, canvasHeight)

    # voeg de cpts toe aan het canvas
    for i, cpt in enumerate(gtl.cpts):
        qcX, rfX, y = scale_cpt_to_canvas(cpt, xScaleCPT, yscale, cpt.groundlevel, top, canvasWidth)
        # tkinter moet een lijst van x,y punten hebben
        qcPoints = list(zip(qcX, y))
        rfPoints = list(zip(rfX, y))
        qcLine = C.create_line(qcPoints, fill="blue")
        rfLine = C.create_line(rfPoints, fill="green")
        cptText = C.create_text(qcPoints[0], text=cpt.testid)

    # voeg de boringen toe aan het canvas
    for i, bore in enumerate(gtl.bores):

        xs, uppers, lowers = scale_bore_to_canvas(bore, yscale, bore.groundlevel, top, canvasWidth)
        colors = bore.soillayers["plotColor"]

        for x, upper, lower, color in list(zip(xs, uppers, lowers, colors)):
            point_from = (x, upper)
            point_to = (x, lower)
            print(point_from, point_to)
            layer_line = C.create_line(x, upper, x, lower, fill=color, width=5)

    # voeg het maaiveld toe aan het canvas
    xs, ys = scale_groundlevel_to_canvas(gtl, yscale, top, canvasWidth)
    groundlevelPoints = list(zip(xs, ys))
    groundlevel_line = C.create_line(groundlevelPoints)

    i = 2
    quitbutton = tk.Button(root, text="Quit", command=finish).pack()

    C.pack()

    # de linker muisknop is Button 1, een klik voegt een punt toe aan een lijn (grens)
    root.bind("<Button 1>", draw_line)

    # de rechter muisknop is button 2 of button 3, een klik maakt een nieuwe lijn (grens)
    line = root.bind("<Button 2>", add_line)
    line = root.bind("<Button 3>", add_line)

    # klik x om het laatste punt te verwijderen
    root.bind("x", remove_last_point)

    root.mainloop()

# instellen van variabelen
canvasWidth = 1800 # breedte van canvas
canvasHeight = 750 # hoogte van canvas
xScaleCPT = 5 # horizontale schaal voor lijnen van cpt op canvas

create_canvas_with_cpts(gtl, canvasWidth, canvasHeight, xScaleCPT)