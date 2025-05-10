import os
from dotenv import load_dotenv
import googlemaps

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=API_KEY)


def get_google_maps_link(user_location, destination_location, mode="walking"):
    origin = f"{user_location[0]},{user_location[1]}"
    dest = f"{destination_location[0]},{destination_location[1]}"
    return f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={dest}&travelmode={mode}"


def main(userLong, userLat, long, lat):

    user_location = (userLong, userLat)
    destination_location = (long, lat)

    route_url = get_google_maps_link(user_location, destination_location)
    print("Google Maps walking route:")
    print(route_url)


#Mock user location (e.g., user is at Meir in Antwerp)
userLong = 51.2172
userLat = 4.4151
# Mock destination coordinates (e.g., a bar the user selected)
long = 51.2206
lat = 4.4024
if __name__ == "__main__":
    main(userLong, userLat, long, lat)

