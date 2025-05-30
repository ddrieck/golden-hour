#!/usr/bin/env python

import argparse
import datetime
import logging
import logging.handlers
import os
import random
import sys

from golden_hour import configuration, timer, timelapse, bluesky, weather
from golden_hour.location import get_location

logger = logging.getLogger()

def calculate_timelapse_duration(duration, interval, photo_display_rate=30.0):
    # return number of seconds
    return float(duration) / interval / photo_display_rate


def get_random_status_text():
    return random.choice([
        'wow.',
        'holy moly',
        'what a time to be alive',
        'inconceivable',
        'reverse sunrise',
    ])


def get_timelapse_filename(output_dir):
    filename_template = '{output_dir}/timelapse_{date}_{count:03d}.mp4'
    today_str = datetime.date.today().isoformat()
    count = 0
    while True:
        filename = filename_template.format(
            output_dir=output_dir,
            date=today_str,
            count=count,
        )
        if not os.path.exists(filename):
            return filename
        count += 1


def main():
    if sys.stdout.isatty():
        handler = logging.StreamHandler(sys.stdout)
        logger.setLevel(logging.INFO)
    else:
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file',
        default=os.path.expanduser('~/.config/golden-hour.yaml'),
        help='configuration file where to find API keys and location information. '
             'Defaults to ~/.config/golden-hour.yaml'
    )
    parser.add_argument('--duration',
        metavar='seconds',
        type=int,
        default=7200, # 2 hours
        help='duration of timelapse capture',
    )
    # TODO might want to enforce minimum of 3 if using raspi cam
    parser.add_argument('--interval',
        metavar='seconds',
        type=int,
        default=8,
        help='time between captured photos',
    )
    parser.add_argument('--start-before-sunset',
        metavar='minutes',
        type=int,
        default=None,
        help='number of minutes before sunset to start timelapse',
    )
    parser.add_argument('--start-before-sunrise',
        metavar='minutes',
        type=int,
        default=None,
        help='number of minutes before sunrise to start timelapse',
    )
    parser.add_argument('--post-to-bluesky',
        action='store_true',
        default=False,
        help='post video to bluesky',
    )
    parser.add_argument('--skip-timelapse',
        action='store_true',
        default=False,
        help='skip recording the timelapse (useful for debugging)',
    )
    parser.add_argument('--debug',
        action='store_true',
        default=False,
        help='enable debug logging',
    )

    args = parser.parse_args()

    config = configuration.load_configuration(args.config_file)
    location = get_location(config['location'])
    output_dir = os.path.expanduser('~/golden-hour-output')

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    timelapse_filename = get_timelapse_filename(output_dir)

    if args.post_to_bluesky:
        bluesky_credentials = config['bluesky']
        logger.info('verifying bluesky credentials')

        # check the expected length of the video to make sure it's within twitter's rules
        video_duration = calculate_timelapse_duration(args.duration, args.interval)
        logger.info('estimated video length: {} seconds'.format(video_duration))
        if video_duration < 5.0:
            logger.error('Error: Timelapse video will be too short to upload to Bluesky (min 5 seconds)')
            exit(1)
        if video_duration > 60.0:
            logger.error('Error: Timelapse video will be too long to upload to Bluesky (max 30 seconds)')
            exit(2)

    if args.start_before_sunset is not None:
        timer.wait_for_sun_time(location, 'sunset', args.start_before_sunset)

    if args.start_before_sunrise is not None:
        timer.wait_for_sun_time(location, 'sunrise', args.start_before_sunrise)

    if not args.skip_timelapse:
        timelapse.create_timelapse(args.duration, args.interval, timelapse_filename)

    if 'openweather_key' in config:
        openweather_key = config['openweather_key']
        if args.start_before_sunset is not None:
            time_of_day = 'sunset'
        else:
            time_of_day = 'sunrise'
        
        time = timer.get_today_sun_time(location, time_of_day)
        forecast = weather.get_sun_forecast(
            openweather_key,
            latitude=location.latitude,
            longitude=location.longitude)
        current = weather.get_current_weather(
            openweather_key,
            latitude=location.latitude,
            longitude=location.longitude
        )
        status_text = weather.get_status_text(forecast, current, time, time_of_day)
    else:
        status_text = get_random_status_text()

    logger.info(status_text)

    if args.post_to_bluesky and not args.skip_timelapse:
        bluesky.post_update(
            config['bluesky'],
            status_text,
            media=timelapse_filename
        )
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('debug logging enabled')

        test_status_text = "TEST POST:\n" + status_text
        bluesky.post_update(
            config['bluesky'],
            test_status_text,
            media=os.path.expanduser('~/.config/golden-hour-debug.mp4'),
            debug=True
        )

    logger.info('done!')


if __name__ == '__main__':
    main()
