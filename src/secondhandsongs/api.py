import requests
from . import models as m
from datetime import datetime
from time import sleep
import logging
from diskcache import Cache

BASE_URI = 'https://secondhandsongs.com/%s'
PREVIOUS_REQUESTS = []
cache = Cache("cachedir")


class Api:

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.set_throughput_rates()

    def get_artist(self, artist_id):
        ret = self.get('artist', str(artist_id))
        return m.Artist(self, ret)

    def get_performance(self, performance_id):
        ret = self.get('performance', str(performance_id))
        return m.Performance(self, ret.json())

    def get_work(self, work_id):
        ret = self.get('work', str(work_id))
        return m.Work(self, ret.json())

    def get_release(self):
        # TODO: to be implemented
        pass

    def get_label(self):
        # TODO: to be implemented
        pass

    #@cache.memoize()
    def get(self, namespace, idx):
        url = '%s/%s' % (namespace, idx)
        headers = {'Accept': 'application/json',
                   'X-Api-Key': self.api_key}
        self._check_throughput_rate()
        PREVIOUS_REQUESTS.append(datetime.now())
        return requests.get(BASE_URI % url, headers=headers)

    def _check_throughput_rate(self):
        t = datetime.now()

        hrs = [(t - x).seconds for x in PREVIOUS_REQUESTS]
        hrs = [s for s in hrs if s < 3600]
        if len(hrs) >= self.reqs_per_hour + 1:
            sleep_time = 3600 - max(hrs)
            logging.warn("Reqs per Hour Exceeded. Sleeping f{sleep_time}s")
            sleep(sleep_time)
            logging.warn("Resuming...")

        secs = [(t - x).seconds for x in PREVIOUS_REQUESTS]
        secs = [s for s in secs if s < 60]

        if len(secs) >= self.reqs_per_minute + 1:
            sleep_time = 60 - max(secs)
            logging.warn("Reqs per Minute Exceeded. Sleeping f{sleep_time}s")
            sleep(sleep_time)
            logging.warn("Resuming...")

        s = 0
        sleep(s)

    def set_throughput_rates(self):
        self.reqs_per_minute = 10
        self.reqs_per_hour = 100
        if self.api_key is not None:
            self.reqs_per_minute = 100  # ?
            self.reqs_per_hour = 1000  # ?
