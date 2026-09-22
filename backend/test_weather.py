from backend.services.geocoding import geocode_location
from backend.services.open_meteo import get_weather


location = "Bangalore"

location_data = geocode_location(location)

print("\n========== LOCATION ==========")
print(location_data)

weather = get_weather(
    location_data["latitude"],
    location_data["longitude"],
)

print("\n========== CURRENT WEATHER ==========")
print(weather.get("current"))

print("\n========== HOURLY WEATHER ==========")
print(weather.get("hourly"))

print("\n========== DAILY WEATHER ==========")
print(weather.get("daily"))