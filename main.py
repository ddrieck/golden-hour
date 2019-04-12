#!/usr/bin/env python

import argparse
import datetime
import logging
import logging.handlers
import os
import random
import sys

from goldenhour import sunset, timelapse, twitter, weather

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
        logger.setLevel(logging.DEBUG)
    else:
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser()
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
    parser.add_argument('--post-to-twitter',
        action='store_true',
        default=False,
        help='post video to twitter',
    )
    parser.add_argument('--darksky-key',
        help='API key for the Dark Sky API'
    )
    parser.add_argument('--skip-timelapse',
        action='store_true',
        default=False,
        help='skip recording the timelapse (useful for debugging)',
    )
    args = parser.parse_args()

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    timelapse_filename = get_timelapse_filename(output_dir)

    if args.post_to_twitter:
        logger.info('verifying twitter credentials')
        twitter.verify_credentials()
        # check the expected length of the video to make sure it's within twitter's rules
        video_duration = calculate_timelapse_duration(args.duration, args.interval)
        logger.info('estimated video length: {} seconds'.format(video_duration))
        if video_duration < 5.0:
            logger.error('Error: Timelapse video will be too short to upload to Twitter (min 5 seconds)')
            exit(1)
        if video_duration > 30.0:
            logger.error('Error: Timelapse video will be too long to upload to Twitter (max 30 seconds)')
            exit(2)

    if args.start_before_sunset is not None:
        sunset.wait_for_sunset(args.start_before_sunset)

    if not args.skip_timelapse:
        timelapse.create_timelapse(args.duration, args.interval, timelapse_filename)

    if args.darksky_key:
        darksky_key = args.darksky_key
        SEATTLE = 47.602, -122.332
        sunset_time = sunset.get_today_sunset_time(sunset.ASTRAL_CITY_NAME_SEATTLE)

        forecast = weather.get_sunset_forecast(darksky_key, sunset_time, SEATTLE)
        status_text = weather.get_status_text(forecast, sunset_time)
    else:
        status_text = get_random_status_text()

    logger.info(status_text)

    if args.post_to_twitter and not args.skip_timelapse:
        twitter.post_update(status_text, media=timelapse_filename)

    logger.info('done!')


if __name__ == '__main__':
    main()
