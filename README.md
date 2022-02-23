# lengteprofiel

## Dependencies
- See environment.yml
- cpt_reader

## Instruction

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
