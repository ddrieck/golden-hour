import yaml
from atproto import Client
import logging
import schema

logger = logging.getLogger(__name__)

def load_credentials_from_file(filepath):
    ''' Load credentials from a YAML file.
    Supports files with bluesky configuration parameters under a "bluesky" key, or at the top level.
    Expects the parameters to match the format of BLUESKY_CONFIG_SCHEMA.
    '''
    with open(filepath) as bluesky_conf_file:
        conf = yaml.load(bluesky_conf_file.read())

    return BLUESKY_CONFIG_SCHEMA.validate(
        conf['bluesky'] if 'bluesky' in conf else conf
    )

def verify_credentials(credentials):
    try:
        client = Client()
        client.login(credentials['identifier'], credentials['password'])
        return True
    except Exception as e:
        logger.error(f"Credential verification failed: {e}")
        return False

BLUESKY_CONFIG_SCHEMA = schema.And(
    {
        'identifier': str,
        'password': str
    },
    verify_credentials
)

def post_update(credentials, text, media=None):
    

    media_id = None
    if media:
        with open(media, 'rb') as mediafile:
            media_id = api.UploadMediaChunked(mediafile)

    api.PostUpdate(text, media=media_id)

def authenticate(username, password):
    client = Client()
    client.login(username, password)
    return client

def validate_config(config_path):
    logger.debug(f"Loading config from {config_path}")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    required_keys = ['username', 'password', 'api_url']
    for key in required_keys:
        if key not in config:
            logger.error(f"Missing required config key: {key}")
            raise ValueError(f"Missing required config key: {key}")
    
    logger.info("Config validation successful")
    return config

def debug_authentication(client):
    try:
        feed = client.get_feed()
        if feed:
            logger.info("Authentication test successful")
            return True
    except Exception as e:
        logger.error(f"Debug authentication failed: {e}")
        return False

def post_update(config_path, status_text, video_path, debug=False):
    logger.info(f"Attempting to post update with video: {video_path}")
    config = validate_config(config_path)
    client = authenticate(config['identifier'], config['password'])

    BLUESKY_CONFIG_SCHEMA.validate(credentials)

    logger.info('posting to bluesky (status_text: {}, media: {})'.format(text, media))
    api = bluesky.Api(**credentials)
    
    if debug:
        if not debug_authentication(client):
            logger.error("Debug authentication check failed")
            return "Debug authentication failed"
    
    try:
        with open(video_path, 'rb') as video_file:
            video_data = video_file.read()
        
        response = client.create_post(status_text, video_data)
        if response.status_code == 201:
            return "Success"
        else:
            return "Failure"
    except Exception as e:
        logger.error(f"Failed to post video: {e}")
        return "Failure"