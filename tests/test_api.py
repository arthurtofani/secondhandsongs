import pytest
import sys
import os

sys.path.append('src')

from dotenv import load_dotenv
from secondhandsongs import Api

__author__ = "Arthur Tofani"
__copyright__ = "Arthur Tofani"
__license__ = "MIT"

load_dotenv()

API_KEY = os.getenv('SHS_API_KEY')

def test_get_performance_with_api_key():
    api = Api(api_key=API_KEY)
    p = api.get_performance(290542)
    assert(p.youtube_url[:23], 'https://www.youtube.com')
    assert(p.spotify_url[:24], 'https://open.spotify.com')

def test_get_performance_without_api_key():
    api = Api(api_key=None)
    p = api.get_performance(290542)
    assert(p.youtube_url, None)
    assert(p.spotify_url, None)
