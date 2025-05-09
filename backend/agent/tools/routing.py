import googlemaps
import json
import random
from dotenv import load_dotenv
import os
from geopy.distance import geodesic

load_dotenv()

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=API_KEY)

# User location (Groenplaats in Antwerp)
user_location = (51.2206, 4.4024)


def load_cafes_data():
    with open("data/maps_dataset/cafe.json", "r", encoding="utf-8") as f:
        cafes = json.load(f)
    return cafes


def get_nearby_cafes(cafes, user_location, max_distance_km=1.0):
    nearby = []
    for cafe in cafes:
        try:
            location = (cafe['lat'], cafe['lon'])
            if geodesic(user_location, location).km <= max_distance_km:
                nearby.append(cafe)
        except Exception:
            continue
    return nearby


def choose_cafe(cafes):
    # For now, pick a random one
    return random.choice(cafes) if cafes else None


def get_cafe_info(cafe):
    try:
        tags = json.loads(cafe.get('tags', '{}'))
        name = tags.get('name', "Unnamed Cafe")
        location = (cafe['lat'], cafe['lon'])
        return name, location
    except Exception:
        return "Unnamed Cafe", (None, None)


def get_google_maps_link(user_location, cafe_location):
    origin = f"{user_location[0]},{user_location[1]}"
    dest = f"{cafe_location[0]},{cafe_location[1]}"
    mode = "walking"
    url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={dest}&travelmode={mode}"  # noqa
    return url


def main():
    cafes = load_cafes_data()
    nearby_cafes = get_nearby_cafes(cafes, user_location, max_distance_km=1.0)
    selected_cafe = choose_cafe(nearby_cafes)

    if selected_cafe:
        cafe_name, cafe_location = get_cafe_info(selected_cafe)
        print(f"Selected Cafe: {cafe_name} at {cafe_location}")
        url = get_google_maps_link(user_location, cafe_location)
        print(f"Google Maps route link: {url}")
    else:
        print("No nearby cafés found within 1 km.")


if __name__ == "__main__":
    main()
