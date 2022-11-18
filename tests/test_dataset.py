from dotenv import load_dotenv
import sys
import os
sys.path.append('src')


from secondhandsongs.dataset import Dataset
from secondhandsongs import Api

load_dotenv()

API_KEY = os.getenv('SHS_API_KEY')
STOPWORDS = ['Angels', 'Bethlehem', 'Christmas', 'Santa', 'Claus',
             'Medley', 'Merry', 'Rudolph', 'Silent Night', 'God',
             'Bells', 'Nosed', 'Glory', 'Pachelbel', 'Jesus',
             'Greensleeves', 'Snowman', 'Noel', 'Noël', ]


def test_get_performance():
    ds = Dataset()
    api = Api(api_key=API_KEY)
    output_folder = '/data/csi/datasets/shs'
    ds.create_slice('slice.csv', output_folder, api, num_items=80,
                    cluster_size=40,
                    stopwords=STOPWORDS)
