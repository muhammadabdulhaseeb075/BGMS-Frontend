import requests
import shapefile

def run(*args):
    tenant = args[0]
    environment = args[1]
    location = args[2]
    if not tenant or not environment or not location:
        print("Missing Args in the Script")
        return
    if environment == 'development':
        r = requests.get('http://' + tenant + '.burialgrounds.co.uk:8000/mapmanagement/mapSearch/?search_type=grave&fuzzy_value=100&purpouse=download_shapefile')
    elif environment == 'staging':
        r = requests.get('https://' + tenant + '.burialgrounds.co.uk:81/mapmanagement/mapSearch/?search_type=grave&fuzzy_value=100&purpouse=download_shapefile')
    elif environment == 'prod':
        r = requests.get('https://' + tenant + '.burialgrounds.co.uk/mapmanagement/mapSearch/?search_type=grave&fuzzy_value=100&purpouse=download_shapefile')
    try:
        response = r.json()
        file = location + tenant + "graves"
        with shapefile.Writer(file) as w:
            w.autoBalance = 1
            w.field('grave_number', 'C')
            for grave in response:
                if grave['topopolygon_id']:
                    grave_number = 0
                    if grave['graveref__grave_number']:
                        grave_number = grave['graveref__grave_number']
                    geo = {
                        "type": "FeatureCollection",
                        "features": grave['topopolygon_centroid'],
                        "properties": grave_number
                    }
                    w.point(geo['features'][0], geo['features'][1])
                    w.record(geo['properties'])
            w.close()
            print("Shapefile saved successfully.")
    except Exception as e:
        print("error writing in the shapefile.")
        print(e)
