import requests

response = requests.get("https://wttr.in/Haldia?format=j1")

data = response.json()

temp = data['current_condition'][0]['temp_C']
feels_like = data['current_condition'][0]['FeelsLikeC']
weather_desc = data['current_condition'][0]['weatherDesc'][0]['value']
humidity = data['current_condition'][0]['humidity']
wind_speed = data['current_condition'][0]['windspeedKmph']
visibility = data['current_condition'][0]['visibility']


print(f"Temperature: {temp}°C")
print(f"Feels like: {feels_like}°C")
print(f"Condition: {weather_desc}")
print(f"Humidity: {humidity}%")
print(f"Wind Speed: {wind_speed} km/h")
print(f"Visibility: {visibility} km")


#print(data)
#print(data['current_condition'][0].keys())