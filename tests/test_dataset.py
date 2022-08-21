import pytest
import sys
import os
sys.path.append('src')

from dotenv import load_dotenv
from secondhandsongs.dataset import Dataset
from secondhandsongs import Api

load_dotenv()

API_KEY = os.getenv('SHS_API_KEY')
STOPWORDS = ['Angels', 'Bethlehem', 'Christmas', 'Santa', 'Claus', 'Medley', 'Merry', 'Rudolph', 'Silent Night', 'God', 'Bells', 'Nosed', 'Glory', 'Pachelbel', 'Jesus', 'Greensleeves', 'Snowman', 'Noel', 'Noël', ]

def test_get_performance():
    ds = Dataset()
    api = Api(api_key=API_KEY)
    ds.create_slice('slice.csv', api, num_queries=30,
                    cluster_size=25,
                    total_tracks=6,
                    stopwords=STOPWORDS)

