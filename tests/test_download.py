import pytest
import sys
import os

sys.path.append('src')

from dotenv import load_dotenv
from secondhandsongs import download as dl

__author__ = "Arthur Tofani"
__copyright__ = "Arthur Tofani"
__license__ = "MIT"

load_dotenv()

# API_KEY = os.getenv('SHS_API_KEY')

def test_download():
    output_folder = '/data/csi/datasets/shs'
    dl.yt_download('slice.csv', output_folder)
