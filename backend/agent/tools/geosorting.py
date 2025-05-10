import json
import os
from geopy.distance import geodesic

def load_dataset(category):
    path = f"data/maps_dataset/{category}.json"
    if not os.path.exists(path):
        raise FileNotFoundError(f"No dataset found for category: {category}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def sort_locations_by_distance(locations, user_location):
    result = []
    for loc in locations:
        try:
            place_location = (loc['lat'], loc['lon'])
            distance = geodesic(user_location, place_location).km
            loc['distance_km'] = distance
            result.append(loc)
        except Exception:
            continue
    return sorted(result, key=lambda x: x['distance_km'])

def yes_no(tag_value):
    if not tag_value:
        return "Unknown"
    value = tag_value.lower()
    return "Yes" if value == "yes" else "No" if value == "no" else value

def get_place_info(loc):
    try:
        tags = json.loads(loc.get('tags', '{}'))
        name = tags.get('name', "Unnamed Location")
        opening_hours = tags.get('opening_hours', "Opening hours not listed")
        internet = yes_no(tags.get('internet_access'))
        outdoor_seating = yes_no(tags.get('outdoor_seating'))
        indoor_seating = yes_no(tags.get('indoor_seating'))
        wheelchair = yes_no(tags.get('wheelchair'))
    except Exception:
        name = "Unnamed Location"
        opening_hours = "Opening hours not listed"
        internet = outdoor_seating = indoor_seating = wheelchair = "Unknown"

    return {
        'id': loc.get('id'),
        'name': name,
        'distance_km': round(loc.get('distance_km', 0.0), 3),
        'opening_hours': opening_hours,
        'internet_access': internet,
        'outdoor_seating': outdoor_seating,
        'indoor_seating': indoor_seating,
        'wheelchair_accessible': wheelchair
    }


def main(category):
    long = 51.2206
    lat = 4.4024
    user_location = (long, lat)

    try:
        locations = load_dataset(category)
        sorted_places = sort_locations_by_distance(locations, user_location)
        structured_results = []

        for place in sorted_places:
            info = get_place_info(place)
            structured_results.append(info)

        return structured_results  # json serializable python object
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    results = main()
    print(json.dumps(results, indent=2, ensure_ascii=False))
