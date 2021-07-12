import datetime
import logging
import math
import time

from astral import Astral
import pytz


logger = logging.getLogger()


def get_current_time_in_timezone(location):
    return datetime.datetime.now(
        pytz.timezone(location.timezone)
    )

def get_today_sun_time(location, time_of_day):
    today = get_current_time_in_timezone(location).date()
    if time_of_day == 'sunset':
        return location.sun(today)['sunset']
    else:
        return location.sun(today)['sunrise']

def get_seconds_until(earlier_time, later_time):
    tdelta = later_time - earlier_time
    return tdelta.total_seconds()

def wait_for_sun_time(location, time_of_day, minutes_before=0):
    sun_time = get_today_sun_time(location, time_of_day)
    start_time = sun_time - datetime.timedelta(minutes=minutes_before)

    now = get_current_time_in_timezone(location)
    if start_time < now:
        logger.error('ERROR: too late to start for today\'s' + time_of_day)
        exit()

    sleep_seconds = get_seconds_until(now, start_time)
    hours = math.floor(sleep_seconds // (60 * 60))
    minutes = math.floor((sleep_seconds // 60) % 60)
    seconds = math.floor(sleep_seconds % 60)
    logger.info(
        'Waiting {hours} {minutes} {seconds} to start, {minutes_before} minutes before {sun_time}'.format(
            sun_time = time_of_day,
            hours='{} hours'.format(hours) if hours > 0 else '',
            minutes='{} minutes'.format(minutes) if minutes > 0 else '',
            seconds='{} seconds'.format(seconds),
            minutes_before=minutes_before,
        )
    )
    time.sleep(sleep_seconds)