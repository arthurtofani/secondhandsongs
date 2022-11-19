# This script creates the train and test datasets as presented in
# http://millionsongdataset.com/secondhand

import requests
from tqdm import tqdm
import pandas as pd
import secondhandsongs as shs
from secondhandsongs.dataset import COLS
from dotenv import load_dotenv

TRAIN_URL = 'https://raw.githubusercontent.com/tbertinmahieux/MSongsDB/master/Tasks_Demos/CoverSongs/shs_dataset_train.txt'
TEST_URL = 'https://raw.githubusercontent.com/tbertinmahieux/MSongsDB/master/Tasks_Demos/CoverSongs/shs_dataset_test.txt'

def get_ids(dt):
    r = [x for x in dt.split('\n') if len(x) > 0 and x[0] not in ['%', '#']]
    r = [int(x.split('<SEP>')[-1]) for x in r]
    return [x for x in r if x > 0]

def load_performances(dt):
    not_found = []
    ps = []
    for pid in tqdm(dt, total=len(dt)):
        try:
            p = api.get_performance(pid)
            ps.append(p)
        except KeyError:
            not_found.append(pid)
    return ps, not_found

def load(api, url, csv_file, limit=None):
    ids = get_ids(requests.get(url).text)[:limit]
    ps, err = load_performances(ids)
    rows = [(p.work_ids[0], p.id, p.title, p.youtube_url) for p in ps]
    df = pd.DataFrame(rows, columns=COLS)
    df.to_csv(csv_file, index=False)
    print("File generated: ", csv_file)


api = shs.Api(api_key=SHS_API_KEY)
load(api, TRAIN_URL, 'shs_train.csv')
load(api, TEST_URL,  'shs_test.csv')
