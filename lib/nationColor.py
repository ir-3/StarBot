import json, requests

markerFilenames = [
	"Aecor",
	"Trunkadis",
	"QuodCanis",
	"Collis",
	"Titus",
	"Arbusto",
	"Sakaro",
	"CerusAlpha",
	"Harenum",
	"Terram",
	"Porrus",
	"Koryza",
	"CerusBeta",
	"Orcus",
	"Syre",
	"Demargos",
	"Remalie"
]

def getNationColor(nation):
	if nation == "None": return int("FFFFFF", 16)

	colors = []

	for world in markerFilenames:
		worldData = json.loads(requests.get(f"https://dynmap.starlegacy.net/tiles/_markers_/marker_{world}.json").content)["sets"]["nations"]["areas"]

		for territory in worldData:
			territoryData = worldData[territory]

			if nation in territoryData["label"]:
				if territoryData["color"] == "#FF0000": pass
				elif territoryData["color"] == "#008000": pass

				return int(territoryData["color"][1:7], 16)

print(getNationColor("Orovika"))