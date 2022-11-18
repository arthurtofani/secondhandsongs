import requests
from bs4 import BeautifulSoup
from . import download as dl
from tqdm import tqdm
import pandas as pd

STATS_URL = "https://secondhandsongs.com/statistics/stats_work_covered?pageSize=%s"
DEFAULT_SKIP = 20
COLS = ['work_id', 'performance_id', 'title', 'url']


class Dataset:

    def create_slice(self, csv_file, output_folder, api, num_items=30,
                     cluster_size=11, stopwords=[]):
        df_out = pd.DataFrame(columns=COLS)
        works = self.get_work_ids(num_items, skip=DEFAULT_SKIP)
        for work_id in tqdm(works, total=len(works)):
            w = api.get_work(work_id)
            self._get_performance_versions(w, df_out, api, cluster_size,
                                           stopwords, output_folder)
            df_out.to_csv(csv_file, index=False)

    def _get_performance_versions(self, work, df_out, api,
                                  num_links, stopwords, output_folder):
        performances = []
        stopwset = set(stopwords)
        invalid_list = dl.get_invalid_list(output_folder)
        for v in work.versions:
            performance_id = v['uri'].split('/')[-1]
            p = api.get_performance(performance_id)
            if performance_id in invalid_list:
                continue
            if p.youtube_url:
                if len(set(p.title.split(' ')).intersection(stopwset)) > 0:
                    return None
                performances.append(p)
                if len(performances) == num_links:
                    for pp in performances:
                        df_out.loc[len(df_out)] = [work.id, pp.id,
                                                   pp.title,
                                                   pp.youtube_url]
                    return df_out

    def get_work_ids(self, num_items, skip=0):
        html = BeautifulSoup(self.get_list(num_items + skip).text, features="lxml")
        r = html.find_all("a", {"class": "link-work"})
        return [x.get('href').split('/')[-1] for x in r][skip:]

    def get_list(self, tracks):
        url = STATS_URL % tracks
        return requests.get(url)
