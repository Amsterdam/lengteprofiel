# lengteprofiel
Script om CPT en geotechnische boringen in GEF of BRO XML format te plotten in een geotechnisch lengteprofiel
Ook is er een point & click interface om profielen met lagen te maken. Deze worden geproduceerd in png, svg en in .geo format dat gebruikt kan worden in DSerie

## Dependencies
- Zie environment.yml
- gefxml_reader

## Instruction for only plotting cpts and bores
1. Put cpts together in a folder _cptPath_  
2. Put bores together in another folder _borePath_  
3. Set a _filename_
4. Run code  
5. PNG and SVG files are created in the same folder
`fileList = os.listdir(cptPath)`  
`fileList = [cptPath + f for f in fileList]`  
`multicpt = Cptverzameling()`  
`multicpt.load_multi_cpt(fileList)`  
`fileList = os.listdir(borePath)`  
`fileList = [borePath + f for f in fileList]`  
`multibore = Boreverzameling()`  
`multibore.load_multi_bore(fileList)`  
`gtl = GeotechnischLengteProfiel()`  
`gtl.set_line(line)`  
`gtl.set_cpts(multicpt)`  
`gtl.set_bores(multibore)`  
`gtl.project_on_line()`  
`gtl.set_groundlevel()`  
`gtl.plot(boundaries={}, filename=filename)`  

## Instructie voor het maken van een profiel met lagen
Invoer:
- sonderingen, als XML of GEF in een map met de naam cpts in dezelfde directory als de code
- profiellijn, als geojson bestand
- lagen, als excel tabel met de naam layers.xlsx in dezelfde directory als de code
    de tabel heeft kolommen laag (nummer in dezelfde volgorde als je getekend hebt), materiaal, kleur (kleurnamen in het Engels)

Run het script _geotechnisch_lengteprofiel.py_