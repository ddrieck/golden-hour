from astral import LocationInfo
from astral.sun import sun 

import schema

# Lowest reasonable elevation is Death Valley, about 100m below sea level.
LOWEST_ALLOWED_ELEVATION = -100

LOCATION_CONFIG_SCHEMA = schema.Schema(
    # Location configuration can either be:
    schema.Or(
        # A string that Astral recognizes (see https://astral.readthedocs.io/en/latest/#cities)
        str,
        # or the lat/lon/timezone/elevation parts we need to create an Astral object
        {
            'latitude': schema.And(schema.Use(float), lambda lat: -90 < lat < 90),
            'longitude': schema.And(schema.Use(float), lambda lon: -180 < lon < 180),
            'timezone': str,
            'elevation': schema.And(schema.Use(float), lambda elevation: elevation >= LOWEST_ALLOWED_ELEVATION),
        }
    )
)


def get_location(location_config):
    ''' return an Astral location object based on the configured location '''
    LOCATION_CONFIG_SCHEMA.validate(location_config)

    if type(location_config) == str:
        # This should be a string that Astral recognizes out of the box
        return LocationInfo()[location_config]
    else:
        location = LocationInfo()
        location.latitude = location_config['latitude']
        location.longitude = location_config['longitude']
        location.timezone = location_config['timezone']
        location.elevation = location_config['elevation']
        return location
