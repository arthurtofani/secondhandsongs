import pytest
import sys
sys.path.append('src')

from secondhandsongs.dataset import Dataset
from secondhandsongs import Api

load_dotenv()

API_KEY = os.getenv('SHS_API_KEY')


def test_get_performance():
    ds = Dataset()
    api = Api(api_key=API_KEY)
    ds.create_slice('slice.csv', api, num_queries=2, cluster_size=2, total_tracks=6)
