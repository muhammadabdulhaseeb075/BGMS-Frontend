import json

CRS = { "crs": { "type": "name", "properties": { "name": "EPSG:27700" } } }


def getGeojson(geojson_feature):
    geoj = json.loads(geojson_feature)['geometry']
    geoj.update(CRS)
    return json.dumps(geoj)