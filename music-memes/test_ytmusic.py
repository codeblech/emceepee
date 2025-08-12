#!/usr/bin/env python3
"""Test script to debug YouTube Music thumbnail extraction"""

import logging
import sys
from ytmusic_thumbnail import get_ytmusic_thumbnail

# Configure logging to show all levels
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_url(url):
    print(f"\n{'='*60}")
    print(f"Testing URL: {url}")
    print('='*60)
    
    result = get_ytmusic_thumbnail(url)
    
    if result:
        print(f"\n✅ SUCCESS: Thumbnail saved to {result}")
    else:
        print(f"\n❌ FAILED: Could not extract thumbnail")
    
    return result

if __name__ == "__main__":
    # Test the specific failing URL
    test_urls = [
        "https://music.youtube.com/watch?v=4K6cvc27_CE",
        # Add more test URLs if needed
    ]
    
    for url in test_urls:
        test_url(url)