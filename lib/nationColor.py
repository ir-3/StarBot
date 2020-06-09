import json, requests

markerFilenames = [
    "Arbusto",
    "Aecor",
    "CerusAlpha",
    "CerusBeta",
    "Collis",
    "Harenum",
    "Koryza",
    "Orcus",
    "Porrus",
    "QuodCanis",
    "Syre",
    "Terram",
    "Titus",
    "Trunkadis",
    "Sakaro"
]

def getNationColor(nation):
    if nation == "None": return int("FFFFFF", 16)

    colors = []

    for world in markerFilenames:
        worldData = json.loads(str(requests.get(f"https://dynmap.starlegacy.net/tiles/_markers_/marker_{world}.json").content)[2:-1])["sets"]["nations"]["areas"]

        for territory in worldData:
            territoryData = worldData[territory]

            if nation in territoryData["label"]:
                if territoryData["color"] == "#FF0000": pass
                elif territoryData["color"] == "#008000": pass

                return int(territoryData["color"][1:7], 16)