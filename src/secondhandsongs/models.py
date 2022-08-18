import json
from types import SimpleNamespace

class Base():
    namespace = None
    def __init__(self, api, args):
        self.api = api


class Artist(Base):
    namespace = 'artists'

    def __init__(self, api, args):
        super(Artist, self).__init__(api, args)
        self.common_name = None
        self.picture = None
        self.birth_date = None
        self.death_date = None
        self.home_country = None
        self.comments = None
        self.aliases = []

    def performances(self):
        return []


class Performance(Base):
    namespace = 'performances'

    def __init__(self, api, args):
        super(Performance, self).__init__(api, args)
        self.id = args['uri'].split('/')[-1]
        self.title = args['title']
        self.uri = args['uri']
        self.performer_name = args['performer']['name']
        self.cover_ids = [a['uri'].split('/')[-1] for a in args['covers']]
        self.covers = None
        self.originals = [a['uri'].split('/')[-1] for a in args['originals']]
        self.is_original = args['isOriginal']
        self.has_spotify_link = False
        self.has_youtube_link = False
        self.youtube_url = None
        self.spotify_url = None
        self._get_links(args)

    def get_covers(self):
        return [self.api.get_performance(x) for x in self.cover_ids]

    def get_original(self):
        return self.api.get_performance(self.originals[0])

    def _get_links(self, args):
        external_uri = args.get('external_uri')
        if external_uri is None:
            return
        self._get_yt_link(external_uri, args)
        self._get_sp_link(external_uri, args)

    def _get_yt_link(self, external_uri, args):
        try:
            self.youtube_url = [x['uri'] for x in args.get('external_uri') if x['site'] == 'YouTube'][0]
            self.has_youtube_link = True
        except IndexError:
            pass

    def _get_sp_link(self, external_uri, args):
        try:
            self.spotify_url = [x['uri'] for x in args.get('external_uri') if x['site'] == 'Spotify'][0]
            self.has_spotify_link = True
        except IndexError:
            pass


class Work(Base):
    namespace = 'work'

    def __init__(self, api, args):
        super(Work, self).__init__(api, args)
        self.id = args['uri'].split('/')[-1]
        self.title = args['title']
        self.uri = args['uri']
        self.language = args['language']
        self.versions = args['versions']
