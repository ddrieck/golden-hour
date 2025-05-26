import argparse
import logging
import os
import subprocess

from .ffmpeg import compile_video


logger = logging.getLogger()


def capture(output_dir, duration, interval):
    logger.info('capturing one photo every {interval} seconds for {duration} seconds'.format(
        duration=duration,
        interval=interval,
    ))
    output_pattern = '{}/image%05d.png'.format(output_dir)
    start_number_files = len(os.listdir(output_dir))
    try:
        subprocess.check_call([
            'rpicam-still',
            '-t', str(duration * 1000),
            '-tl', str(interval * 1000),
            '-n', # don't try to show a preview window
            '-w', '1280',
            '-h', '720',
            #'--rotation', '180', # set this to correct for camera orientation
            '--quality', '100',
            # '--verbose',
            # '--saturation', '50',
            '-o', output_pattern,
            '-e', 'png',
        ])
    except subprocess.CalledProcessError as error:
        logger.error('Error encountered while capturing using raspistill', exc_info=True)
    file_list = os.listdir(output_dir)
    end_number_files = len(file_list)
    logger.info('Captured {count} photos'.format(
        count=end_number_files - start_number_files,
    ))


def main():
    parser = argparse.ArgumentParser(description='Record a timelapse.')
    parser.add_argument('--duration', metavar='seconds', required=True, type=int, help='total duration of timelapse capture in seconds')
    parser.add_argument('--interval', metavar='seconds', required=True, type=int, help='number of seconds between photo captures')
    parser.add_argument('--photos-per-second', type=int, default=30, help='number of photos displayed per second in video')
    args = parser.parse_args()
    logger.debug(args)

    # capture and compile timelapse
    if not os.path.exists('photos'):
        os.makedirs('photos')
    photos_dir = os.path.abspath('photos')
    output_filename = 'timelapse.mp4'
    logger.info('created {}'.format(photos_dir))
    capture(photos_dir, args.duration, args.interval)
    compile_video(photos_dir, output_filename, args.photos_per_second)
    # TODO clean up temp dir


if __name__ == '__main__':
    main()
