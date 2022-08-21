import requests
from bs4 import BeautifulSoup
from . import models as m
from tqdm import tqdm
import pandas as pd

STATS_URL = "https://secondhandsongs.com/statistics/stats_work_covered?pageSize=%s"
DEFAULT_SKIP = 20

class Dataset:


    def create_slice(self, output_file, api, num_queries=30, cluster_size=11,
                     total_tracks=1000, stopwords=[]):
        #arr = []
        df_out = pd.DataFrame(columns=['work_id', 'performance_id', 'title', 'url'])
        works = self.get_work_ids(num_queries, skip=DEFAULT_SKIP)
        for work_id in tqdm(works, total=len(works)):
            w = api.get_work(work_id)
            self._get_performance_versions(w, df_out, api, cluster_size, stopwords)
            df_out.to_csv(output_file, index=False)
        import code; code.interact(local=dict(globals(), **locals()))


    def _get_performance_versions(self, work, df_out, api, num_links, stopwords):
            performances = []
            for v in work.versions:
                performance_id = v['uri'].split('/')[-1]
                p = api.get_performance(performance_id)
                if p.youtube_url:
                    if len(set(p.title.split(' ')).intersection(set(stopwords))) > 0:
                        return None
                    performances.append(p)
                    if len(performances) == num_links:
                        for pp in performances:
                            df_out.loc[len(df_out)] = [work.id, pp.id,
                                                       pp.title,
                                                       pp.youtube_url]
                        return df_out



    def get_work_ids(self, num_queries, skip=0):
        html = BeautifulSoup(self.get_list(num_queries + skip).text)
        r = html.find_all("a", {"class": "link-work"})
        return [x.get('href').split('/')[-1] for x in r][skip:]


    def get_list(self, tracks):
        url = STATS_URL % tracks
        return requests.get(url)
