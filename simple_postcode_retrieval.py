import requests
import sys
import psycopg2
import json
from constants import API_KEY,IP_ADDRESS


conn = psycopg2.connect(f"host={IP_ADDRESS} dbname=Postcodes user=postgres password=admin")
cur = conn.cursor()


def get_isolines(api_key, lat, lon, mode, minutes):
    url = "https://api.geoapify.com/v1/isoline"
    params = {
        "apiKey": api_key,
        "lat": lat,
        "lon": lon,
        "type": "time",
        "mode": mode,
        "range": minutes * 60,
    }
    response = requests.get(url, params=params)
    return response.json()

def get_coordinates(api_key, address):
    url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "apiKey": api_key,
        "text": address
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['features']:
        lat = data['features'][0]['geometry']['coordinates'][1]
        lon = data['features'][0]['geometry']['coordinates'][0]
        return lat, lon
    else:
        return None, None
    
def get_postcodes_within_isoline(cur, geojson_feature_collection):
    # Ensure we have features in the collection
    if not geojson_feature_collection['features']:
        return []

    # Extract the geometry from the first feature in the FeatureCollection
    geometry = geojson_feature_collection['features'][0]['geometry']
    geojson_str = json.dumps(geometry)

    # SQL query to fetch postcodes within the GeoJSON polygon
    sql_query = f"""
    SELECT postcode FROM london_postcodes 
    WHERE ST_Intersects(geom, ST_SetSRID(ST_GeomFromGeoJSON('{geojson_str}'), 4326));
    """
    cur.execute(sql_query)
    return cur.fetchall()

def main():
    if len(sys.argv) != 3:
        print("Usage: simple_postcode_retrieval.py <MODE> <MINUTES>")
        sys.exit(1)
    
    address = input("Please enter the address of the point of interest!")
    
    api_key = API_KEY
    lat, lon = get_coordinates(API_KEY, address)
    mode = sys.argv[1]
    minutes = int(sys.argv[2])
    
    isoline_geojson = get_isolines(api_key, lat, lon, mode, minutes)
    print(isoline_geojson)
    print(type(isoline_geojson))
    #isoline_geojson_str = json.dumps(isoline_geojson)
    
    # sql_query = f"SELECT postcode FROM london_postcodes WHERE ST_Intersects(geom, ST_GeomFromGeoJSON('{isoline_geojson_str}'));"
    # cur.execute(sql_query)

    # Fetch and print results
    postcodes = get_postcodes_within_isoline(cur,isoline_geojson)
    for postcode in postcodes:
        print(postcode)

    # Clean up
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
