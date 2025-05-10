import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPEN_WEATHER_API_KEY')

#don't forget to pip install requests in terminal
def get_city_name(latitude, longitude):
    # Reverse geocoding API URL to also get the name of the city you are in, thought it could be handy
    geocode_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': api_key
    }

    response = requests.get(geocode_url, params=params)
    data = response.json()

    if response.status_code == 200:
        # Extract city name from the response!!
        city = data['name']
        return city
    else:
        print("Geocoding error, can't get city name:", data)
        return None

def get_weather(latitude, longitude):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': api_key,
        'units': 'metric'  # metric means in Celsius
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        # Get the city name by calling reverse geocoding
        city_name = get_city_name(latitude, longitude)

        weather = {
            'location': city_name if city_name else f"Lat: {latitude}, Lon: {longitude}",
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather
    else:
        print("Full API response:", data)
        return {"error": data.get("message", "Something went wrong, please try again.")}


if __name__ == "__main__":
    # Actual implementation:
    latitude = 51.2194  # Example latitude for Antwerp
    longitude = 4.4025  # Example longitude for Antwerp
    weather_data = get_weather(latitude, longitude)
    print(weather_data)