import requests
from bs4 import BeautifulSoup
from . import models as m
import pandas as pd

STATS_URL = "https://secondhandsongs.com/statistics/stats_work_covered?pageSize=%s"

class Dataset:

    def create_slice(self, output_file, api, num_queries=30, cluster_size=11,
                     total_tracks=1000):
        arr = []
        for work_id in self.get_work_ids(num_queries):
            w = api.get_work(work_id)
            df = pd.DataFrame.from_dict(w.versions)
            df['performance_id'] = df.uri.str.split('/').apply(lambda x: x[-1])
            df['work_id'] = work_id
            df = df[['work_id', 'title', 'isOriginal', 'performance_id']]
            df_ori = df[df.isOriginal == True]
            df_ver = df[df.isOriginal == False].sample(cluster_size -1)
            arr.append(df_ori)
            arr.append(df_ver)
        df = pd.concat(arr)
        #import code; code.interact(local=dict(globals(), **locals()))


    def get_work_ids(self, num_queries):
        html = BeautifulSoup(self.get_list(num_queries).text)
        r = html.find_all("a", {"class": "link-work"})
        return [x.get('href').split('/')[-1] for x in r]


    def get_list(self, tracks):
        url = STATS_URL % tracks
        return requests.get(url)
