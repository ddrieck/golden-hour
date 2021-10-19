import logging
import subprocess


logger = logging.getLogger()


def compile_video(photos_dir, output_filename, photos_per_second=30):
    logger.info('compiling timelapse (photos per second: {photos_per_second})'.format(
        photos_per_second=photos_per_second,
    ))
    # TODO ensure output_filename ends with .mp4
    photos_pattern = '{}/image%05d.png'.format(photos_dir)
    try:
        subprocess.check_call([
            'ffmpeg',
            '-loglevel', 'warning',
            '-framerate', str(photos_per_second),
            '-i', photos_pattern,
            '-c:v', 'libx264',
            '-r', '30',
            '-b:v 4096'
            '-pix_fmt', 'yuv420p',
            output_filename,
        ])
    except subprocess.CalledProcessError as error:
        logger.error('Error encountered while generating video using ffmpeg', exc_info=True)