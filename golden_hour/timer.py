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

def get_today_sunset_time(location):
    today = get_current_time_in_timezone(location).date()
    return location.sun(today)['sunset']

def get_today_sunrise_time(location):
    today = get_current_time_in_timezone(location).date()
    return location.sun(today)['sunrise']

def get_seconds_until(earlier_time, later_time):
    tdelta = later_time - earlier_time
    return tdelta.total_seconds()


def wait_for_sunset(location, minutes_before=0):
    sunset_time = get_today_sunset_time(location)
    start_time = sunset_time - datetime.timedelta(minutes=minutes_before)

    now = get_current_time_in_timezone(location)
    if start_time < now:
        logger.error('ERROR: too late to start for today\'s sunset')
        exit()

    sleep_seconds = get_seconds_until(now, start_time)
    hours = math.floor(sleep_seconds // (60 * 60))
    minutes = math.floor((sleep_seconds // 60) % 60)
    seconds = math.floor(sleep_seconds % 60)
    logger.info(
        'Waiting {hours} {minutes} {seconds} to start, {minutes_before} minutes before sunset'.format(
            hours='{} hours'.format(hours) if hours > 0 else '',
            minutes='{} minutes'.format(minutes) if minutes > 0 else '',
            seconds='{} seconds'.format(seconds),
            minutes_before=minutes_before,
        )
    )
    time.sleep(sleep_seconds)

def wait_for_sunrise(location, minutes_before=0):
    sunrise_time = get_today_sunrise_time(location)
    start_time = sunrise_time - datetime.timedelta(minutes=minutes_before)

    now = get_current_time_in_timezone(location)
    if start_time < now:
        logger.error('ERROR: too late to start for today\'s sunrise')
        exit()

    sleep_seconds = get_seconds_until(now, start_time)
    hours = math.floor(sleep_seconds // (60 * 60))
    minutes = math.floor((sleep_seconds // 60) % 60)
    seconds = math.floor(sleep_seconds % 60)
    logger.info(
        'Waiting {hours} {minutes} {seconds} to start, {minutes_before} minutes before sunrise'.format(
            hours='{} hours'.format(hours) if hours > 0 else '',
            minutes='{} minutes'.format(minutes) if minutes > 0 else '',
            seconds='{} seconds'.format(seconds),
            minutes_before=minutes_before,
        )
    )
    time.sleep(sleep_seconds)