import os
import random
import time
import logging
from urllib.parse import urlparse
from maker import (
    apply_overlay_transformation_image,
    apply_overlay_transformation_v2_image,
)
from ytmusic_thumbnail import get_ytmusic_thumbnail
from spotify_thumbnail import get_spotify_thumbnail
from youtube_thumbnail import get_yt_thumbnail

logger = logging.getLogger(__name__)


def detect_platform(url):
    """
    Detect the music platform from a URL.

    Args:
        url (str): The URL to analyze

    Returns:
        str: One of 'ytmusic', 'spotify', 'youtube', or 'unknown'
    """
    parsed = urlparse(url.lower())
    domain = parsed.netloc.replace('www.', '').replace('m.', '')

    if 'music.youtube.com' in domain:
        return 'ytmusic'
    elif 'open.spotify.com' in domain:
        return 'spotify'
    elif 'youtube.com' in domain or 'youtu.be' in domain:
        return 'youtube'
    else:
        return 'unknown'


def get_thumbnail_by_platform(url):
    """
    Get thumbnail based on the detected platform.

    Args:
        url (str): The URL to get thumbnail for

    Returns:
        str or None: Path to the downloaded thumbnail, or None if failed
    """
    platform = detect_platform(url)
    logger.info(f"Getting thumbnail for URL: {url}, detected platform: {platform}")

    if platform == 'ytmusic':
        logger.info("Calling get_ytmusic_thumbnail")
        result = get_ytmusic_thumbnail(url)
        if result:
            logger.info(f"YT Music thumbnail downloaded successfully: {result}")
        else:
            logger.error(f"YT Music thumbnail download failed for URL: {url}")
        return result
    elif platform == 'spotify':
        logger.info("Calling get_spotify_thumbnail")
        result = get_spotify_thumbnail(url)
        if result:
            logger.info(f"Spotify thumbnail downloaded successfully: {result}")
        else:
            logger.error(f"Spotify thumbnail download failed for URL: {url}")
        return result
    elif platform == 'youtube':
        logger.info("Calling get_yt_thumbnail")
        result = get_yt_thumbnail(url)
        if result:
            logger.info(f"YouTube thumbnail downloaded successfully: {result}")
        else:
            logger.error(f"YouTube thumbnail download failed for URL: {url}")
        return result
    else:
        logger.error(f"Unknown platform for URL: {url}")
        return None


def get_random_background(num_overlays):
    """
    Get a random background image for the specified number of overlays.

    Args:
        num_overlays (int): Number of overlay images (1-5)

    Returns:
        str or None: Path to the background image, or None if not found
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backgrounds_directory = os.path.join(script_dir, "assets", "background", str(num_overlays))
    
    logger.info(f"Looking for backgrounds in: {backgrounds_directory}")

    if not os.path.exists(backgrounds_directory):
        logger.error(f"Background directory does not exist: {backgrounds_directory}")
        return None

    background_files = [
        f
        for f in os.listdir(backgrounds_directory)
        if os.path.isfile(os.path.join(backgrounds_directory, f))
    ]

    if not background_files:
        return None

    # Seed random with current time for better randomness
    random.seed(time.time())
    background_filename = random.choice(background_files)
    return os.path.join(backgrounds_directory, background_filename)


def generate_meme_image_from_url(url):
    """
    Generate a meme image from a single music URL (supports YT Music, Spotify, YouTube).

    Args:
        url (str): Music URL for a song or playlist

    Returns:
        PIL.Image: Generated meme image, or None if generation failed
    """
    logger.info(f"Generating meme for URL: {url}")
    
    # Get thumbnail from URL (auto-detects platform)
    overlay_path = get_thumbnail_by_platform(url)
    if not overlay_path:
        logger.error(f"Failed to get thumbnail for URL: {url}")
        return None
    logger.info(f"Got overlay path: {overlay_path}")

    # Get random background for single image
    background_path = get_random_background(1)
    if not background_path:
        logger.error("Failed to get random background image")
        return None
    logger.info(f"Got background path: {background_path}")

    # Generate meme and return PIL Image
    try:
        result = apply_overlay_transformation_image(background_path, overlay_path)
        if result:
            logger.info("Meme image generated successfully")
        else:
            logger.error("apply_overlay_transformation_image returned None")
        return result
    except Exception as e:
        logger.error(f"Failed to apply overlay transformation: {e}")
        return None


def generate_meme_image_from_ytmusic_url(ytmusic_url):
    """
    Generate a meme image from a single YT Music URL.
    (Deprecated: Use generate_meme_image_from_url instead)

    Args:
        ytmusic_url (str): YT Music URL for a song or playlist

    Returns:
        PIL.Image: Generated meme image, or None if generation failed
    """
    return generate_meme_image_from_url(ytmusic_url)


def generate_meme_image_from_spotify_url(spotify_url):
    """
    Generate a meme image from a single Spotify URL.

    Args:
        spotify_url (str): Spotify URL for a song or playlist

    Returns:
        PIL.Image: Generated meme image, or None if generation failed
    """
    return generate_meme_image_from_url(spotify_url)


def generate_meme_image_from_youtube_url(youtube_url):
    """
    Generate a meme image from a single YouTube URL.

    Args:
        youtube_url (str): YouTube URL for a video

    Returns:
        PIL.Image: Generated meme image, or None if generation failed
    """
    return generate_meme_image_from_url(youtube_url)


def generate_meme_image_from_urls(urls):
    """
    Generate a single meme image from a list of music URLs (max 5).
    Supports mixed platforms: YT Music, Spotify, YouTube.

    Args:
        urls (list): List of music URLs (max length 5)

    Returns:
        PIL.Image: Generated meme image, or None if generation failed
    """
    if len(urls) > 5:
        raise ValueError("Maximum 5 URLs allowed")

    if len(urls) == 0:
        return None

    # Get thumbnails from URLs (auto-detects platforms)
    overlay_paths = [
        path for url in urls if (path := get_thumbnail_by_platform(url)) is not None
    ]

    if not overlay_paths:
        return None

    n = len(overlay_paths)
    background_path = get_random_background(n)

    if not background_path:
        return None

    # Generate single meme and return PIL Image
    if n == 1:
        return apply_overlay_transformation_image(background_path, overlay_paths[0])
    else:
        return apply_overlay_transformation_v2_image(background_path, overlay_paths)


def generate_meme_image_from_ytmusic_urls(ytmusic_urls):
    """
    Generate a single meme image from a list of YT Music URLs (max 5).
    (Deprecated: Use generate_meme_image_from_urls instead)

    Args:
        ytmusic_urls (list): List of YT Music URLs (max length 5)

    Returns:
        PIL.Image: Generated meme image, or None if generation failed
    """
    return generate_meme_image_from_urls(ytmusic_urls)


def generate_meme_image_from_spotify_urls(spotify_urls):
    """
    Generate a single meme image from a list of Spotify URLs (max 5).

    Args:
        spotify_urls (list): List of Spotify URLs (max length 5)

    Returns:
        PIL.Image: Generated meme image, or None if generation failed
    """
    return generate_meme_image_from_urls(spotify_urls)


def generate_meme_image_from_youtube_urls(youtube_urls):
    """
    Generate a single meme image from a list of YouTube URLs (max 5).

    Args:
        youtube_urls (list): List of YouTube URLs (max length 5)

    Returns:
        PIL.Image: Generated meme image, or None if generation failed
    """
    return generate_meme_image_from_urls(youtube_urls)
