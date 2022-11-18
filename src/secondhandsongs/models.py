class Base():
    namespace = None

    def __init__(self, api, args):
        self.api = api
        self.response = args


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
        self.performer_id = args['performer']['uri'].split('/')[-1]
        self.cover_ids = [a['uri'].split('/')[-1] for a in args['covers']]
        self.covers = None
        self.originals = [a['uri'].split('/')[-1] for a in args['originals']]
        self.work_ids = [a['uri'].split('/')[-1] for a in args['works']]
        self.release_ids = [a['uri'].split('/')[-1] for a in args['releases']]
        self.is_original = args['isOriginal']
        self.has_spotify_link = False
        self.has_youtube_link = False
        self.youtube_url = None
        self.spotify_url = None
        self._get_links(args)

    def get_works(self):
        return [self.api.get_work(x) for x in self.work_ids]

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
            self.youtube_url = self._get_link(args, 'YouTube')
            self.has_youtube_link = True
        except IndexError:
            pass

    def _get_sp_link(self, external_uri, args):
        try:
            self.spotify_url = self._get_link(args, 'Spotify')
            self.has_spotify_link = True
        except IndexError:
            pass

    def _get_link(self, args, svc):
        external_uri = args.get('external_uri')
        return [x['uri'] for x in external_uri if x['site'] == svc][0]


class Work(Base):
    namespace = 'work'

    def __init__(self, api, args):
        super(Work, self).__init__(api, args)
        self.id = args['uri'].split('/')[-1]
        self.title = args['title']
        self.uri = args['uri']
        self.language = args['language']
        self.versions = args['versions']
        self.version_ids = [a['uri'].split('/')[-1] for a in args['versions']]

