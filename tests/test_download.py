import sys
sys.path.append('src')

from dotenv import load_dotenv
from secondhandsongs import download as dl

__author__ = "Arthur Tofani"
__copyright__ = "Arthur Tofani"
__license__ = "MIT"

load_dotenv()


def test_download():
    output_folder = '/data/csi/datasets/shs'
    dl.yt_download('slice.csv', output_folder)
