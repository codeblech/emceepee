# next step: robustness. add code to handle when ytmusc doesnt return deprecation warning.
# more meaningful error handling
# make the filename unique and predictable using better regex to get video id in ytmusic
# check if thumbnail for this song is already there (downloaded)
# use logging module
# use uv package manager

# avoid re-rendering of site on using slider
# give a key to every slider, embed button, audio and video element to make them unique
# add music to youtube music videos
# yt_dlp doesn't work on hosted site
# make a single input box that detects what platform link is pasted


from bs4 import BeautifulSoup
import requests
import os
from PIL import Image
from io import BytesIO
import regex
import logging

logger = logging.getLogger(__name__)


def get_ytmusic_thumbnail(url: str) -> str | None:
    """Get the thumbnail of a song, playlist, or album using its youtube music url

    Args:
        url (str): YouTube Music url to the song

    Returns:
        str | None: path to the downloaded thumbail image file
    """
    logger.info(f"Starting thumbnail extraction for URL: {url}")
    
    # Make request to YouTube Music
    try:
        r = requests.get(url)
        logger.info(f"Request status code: {r.status_code}")
        if r.status_code != 200:
            logger.error(f"Failed to fetch URL. Status code: {r.status_code}")
            return None
    except Exception as e:
        logger.error(f"Request failed with exception: {e}")
        return None

    # Parse HTML
    try:
        soup = BeautifulSoup(r.content, "lxml")
        title_tags = soup.find_all("title")  # ytmusic returns two title tags in html
        logger.info(f"Found {len(title_tags)} title tags")
        
        if title_tags:
            logger.info(f"First title tag content: {str(title_tags[0])[:100]}...")
        else:
            logger.warning("No title tags found in HTML")
    except Exception as e:
        logger.error(f"HTML parsing failed: {e}")
        return None

    # Extract thumbnail URL
    thumbnail_url = None
    if title_tags and "Your browser is deprecated" in str(title_tags[0]):
        logger.info("Found 'Your browser is deprecated' in title - looking for og:image meta tag")
        meta = soup.find("meta", {"property": "og:image"})
        if meta:
            thumbnail_url = meta.get("content", None)
            logger.info(f"Found thumbnail URL: {thumbnail_url}")
        else:
            logger.warning("No og:image meta tag found")
    else:
        # Log what we actually found in the title
        if title_tags:
            logger.warning(f"Title tag doesn't contain expected deprecation warning. Found: {str(title_tags[0])[:200]}")
        logger.info("Trying alternative method - looking for og:image anyway")
        meta = soup.find("meta", {"property": "og:image"})
        if meta:
            thumbnail_url = meta.get("content", None)
            logger.info(f"Found thumbnail URL via alternative method: {thumbnail_url}")

    if thumbnail_url is None:
        logger.error("Could not extract thumbnail URL from page")
        return None

    # Download thumbnail
    try:
        logger.info(f"Downloading thumbnail from: {thumbnail_url}")
        rr = requests.get(thumbnail_url)
        if rr.status_code != 200:
            logger.error(f"Failed to download thumbnail. Status code: {rr.status_code}")
            return None
        logger.info(f"Thumbnail downloaded successfully. Size: {len(rr.content)} bytes")
    except Exception as e:
        logger.error(f"Thumbnail download failed with exception: {e}")
        return None

    # Extract save name from URL
    try:
        regex_result = regex.findall(r".*=(.*)", url)
        if not regex_result:
            logger.error(f"Failed to extract video ID from URL using regex. URL: {url}")
            # Fallback: try to extract just the video ID differently
            if "watch?v=" in url:
                save_name = url.split("watch?v=")[1].split("&")[0]
                logger.info(f"Using fallback method. Extracted video ID: {save_name}")
            else:
                logger.error("Could not extract video ID with fallback method either")
                return None
        else:
            save_name = regex_result[0]
            logger.info(f"Extracted save name via regex: {save_name}")
    except Exception as e:
        logger.error(f"Failed to extract save name: {e}")
        return None

    # Save image
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    thumbnails_dir = os.path.join(script_dir, "assets", "thumbnails", "ytmusic")
    save_path = os.path.join(thumbnails_dir, f"{save_name}.jpg")
    
    try:
        os.makedirs(thumbnails_dir, exist_ok=True)
        logger.info(f"Saving image to: {save_path}")
        
        with Image.open(BytesIO(rr.content)) as im:
            im.save(save_path, format="JPEG")
            logger.info(f"Image saved successfully. Dimensions: {im.size}")
            return save_path
    except Exception as e:
        logger.error(f"Failed to save image: {e}")
        return None


if __name__ == "__main__":
    get_ytmusic_thumbnail(
        "https://music.youtube.com/watch?v=sEetXo3R-aM&si=zEbt0ZqGo_HHwQJ8"
    )
