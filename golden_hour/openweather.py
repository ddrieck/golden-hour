import requests

def get_forecast(openweather_key, lat, long):
    open_weather_url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&units=imperial&exclude=minutely&appid=%s" % (lat, long, openweather_key)
    response = requests.get(open_weather_url)
    forecast = response.json()

    return forecast
    