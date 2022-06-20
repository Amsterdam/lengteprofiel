# lengteprofiel
Scripts om CPT en geotechnische boringen in GEF of BRO XML format te plotten in een geotechnisch lengteprofiel
Er zijn er twee kant en klaar scripts om profielen te maken:
- _plot_cpt_in_lengteprofiel.py_ plot boringen en sonderingen in een lengteprofiel.
- _verwerk_geotechnisch_lengteprofiel.py_ geeft point & click interface om lagen te tekenen bij boringen en sonderingen.
Uitvoer in png, svg en als er lagen zijn gemaakt .geo-format dat gebruikt kan worden in DSerie

## Dependencies
* Zie environment.yml
* [gefxml_reader](https://github.com/Amsterdam/gefxml_viewer)

# Heb je geen ervaring met Python? Volg dan deze stappen

## De applicatie opslaan
1. Voer eerst de stappen uit van de [gefxml_reader](https://github.com/Amsterdam/gefxml_viewer)
1. Ga naar de map _scripts_. Klik met de rechtermuisknop en kies voor _Git bash here_
1. Kopieer en plak (met rechtse muisknop of shift + Insert):
`git clone https://github.com/Amsterdam/lengteprofiel.git`
1. Je kan het Git bash venster nu afsluiten met `exit`
1. Controleer of er in de map _lengteprofiel_ een map is met de naam _input_ en een map _output_

## Input bestanden klaar zetten
1. Maak in GIS een geojson bestand met daarin 1 lijn (mag meer dan 2 punten hebben)
1. Sla het geojson bestand op in de map _input_ als _profiel.geojson_
1. Sla in deze map ook de gef of xml bestanden van de sonderingen en boringen op

## Profielen maken
1. Ga naar de Windows startknop en type daar `cmd`
1. Kies _Anaconda Prompt (Miniconda3)_
1. Ga in de prompt naar de map _lengteprofiel_ 
1. Kopieer en plak:
* `conda activate geo_env` (dit moet je iedere keer doen wanneer je begint met een sessie)
* `python maak_lengteprofiel.py`
1. Kijk in de map _output_ of daar een png en een svg zijn gemaakt

## Vragen of opmerkingen?
1. Stuur een bericht aan Thomas van der Linden, bijvoorbeeld via [LinkedIn](https://www.linkedin.com/in/tjmvanderlinden/)

## Resultaten?
1. Heb je mooie resultaten gemaakt met deze applicatie? We vinden het heel leuk als je ze deelt (en Thomas tagt)
