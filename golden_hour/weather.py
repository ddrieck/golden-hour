# -*- coding: utf-8 -*-
import datetime
from random import choice
from golden_hour.openweather import get_forecast

def get_sunset_forecast(openweather_key, lat, long):
    # Get the forecast from *just before* sunset to avoid night-themed emoji
    forecast = get_forecast(openweather_key, lat, long)

    return forecast

def get_status_text(forecast, sunset_time):
    hourly = forecast['hourly']
    current = forecast['current']

    return '\n'.join(
        filter(None, [
            '🌅 sunset at {}\n'.format(sunset_time.strftime('%I:%M%p')),
            summary(hourly, current),
            temp(current),
            cloudiness(current),
            precip(hourly, current),
            wind(current),
            visibility(current),
        ])
    )


def summary(hourly, current):
    summ = hourly[0]['weather'][0]["description"]

    icon = current['weather'][0]['icon']
    cloud_cover = current['clouds']
    temperature = current['temp']

    return '{} {}'.format(
        get_emoji(icon, temperature, cloud_cover),
        summ.lower()
    )

def temp(current):
    temperature = current['temp']
    feels_like = current['feels_like']

    feels_like = (
        ''
        if round(temperature) == round(feels_like)
        else ' (feels like {})'.format(display_temp(feels_like))
    )

    return '🌡 {}{}'.format(
        display_temp(temperature),
        feels_like
    )


def cloudiness(current):
    cloud_cover = current['clouds']

    if cloud_cover > 1:
        return '{} {}% cloud cover'.format(
            get_cloud_cover_emoji(cloud_cover),
            round(cloud_cover)
        )

def precip(hourly,current):
    cloud_cover = current['clouds']

    precip_prob = hourly[0]['pop']
    status_main = hourly[0]['weather'][0]['main'].lower()
    precip_type = ''
    
    if status_main == 'clouds':
        precip_type == 'rain'
    else:
        precip_type == status_main


    if precip_type and precip_prob > 0:
        return  '{} {}% chance of {}'.format(
            get_precip_emoji(precip_type, cloud_cover),
            round(precip_prob * 100),
            precip_type
        )

def wind(current):
    wind_speed = current['wind_speed']
    wind_bearing = current['wind_deg']

    if wind_speed > 5:
        return '💨 winds about {}mph from the {}'.format(
            round(wind_speed),
            get_bearing(wind_bearing)
        )

def visibility(current):
    vis = int(current['visibility'])
    vis = vis * 0.00062137119223733
    
    if vis < 5:
        return '🌁 {} miles of visibility'.format(vis)

def display_temp(temperature):
    degrees = '℉'

    return str(round(temperature)) + degrees


def get_emoji(icon, temperature, cloud_cover):
    if icon == '01d':
        if temperature > 75:
            return choice(['☀️', '☀️', '😎'])

        if temperature < 32:
            return choice(['☀️', '☀️', '⛄️'])

        return '☀️'

    if icon == '10d' or icon == '09d':
        if cloud_cover < 50:
            return choice(['🌧', '☔️', '🌦'])

        return choice(['🌧', '☔️'])

    return {
        '01n': '🌝',
        '13d': choice(['❄️', '🌨', '☃️']),
        '50d': '🌁',
        '04d': '☁️',
        '02d': '🌤',
        '02n': '⛅️',
    }.get(icon, '')


def get_cloud_cover_emoji(cloud_cover):
    if cloud_cover < 20:
        return '☀️'

    if cloud_cover < 50:
        return '🌤'

    if cloud_cover < 90:
        return '🌥'

    return '☁️'


def get_precip_emoji(precip_type, cloud_cover):
    if precip_type == 'rain':
        if (cloud_cover < 50):
            return choice(['🌧', '☔️', '🌦'])

        return choice(['🌧', '☔️'])

    if precip_type == 'snow':
        return choice(['❄️', '🌨', '☃️'])

    if precip_type == 'thunderstorm':
        return '🌨'

    return ''

def get_bearing(degrees, short = False):
    directions = (
        'N,NNE,NE,ENE,E,ESE,SE,SSE,S,SSW,SW,WSW,W,WNW,NW,NNW'
        if short
        else 'north,northeast,east,southeast,south,southwest,west,northwest'
    ).split(',')

    count = len(directions)

    # Distance between each direction
    span = 360.0 / count

    # Use modulo to "round" `16` to `0`
    index = round(degrees / span) % count

    return directions[index]
