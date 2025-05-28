import requests

def get_forecast(openweather_key, latitude, longitude):
    open_weather_url = "https://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&units=imperial&exclude=minutely&appid=%s" % (latitude, longitude, openweather_key)
    response = requests.get(open_weather_url)
    forecast = response.json()

    return forecast    

def get_current(openweather_key, latitude, longitude):
    open_weather_url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&units=imperial&exclude=minutely&appid=%s" % (latitude, longitude, openweather_key)
    response = requests.get(open_weather_url)
    current = response.json()

    return current    