# SecondHandSongs.com Python API Wrapper

Python API Wrapper for SecondHandSongs.com API



----------------------

## Features:

* Supports SHS API key
* Automatic throttle control
* Cached requests
* Download Youtube and Spotify content (may require specific API keys)


## Requirements

```
pip install secondhandsongs
```


## Using the SecondHandSongs.com API

#### Get performances
```python

from secondhandsongs import Api

def print_performance(p):
    print("id:", p.id)
    print("title:", p.title)
    print("uri:", p.uri)
    print("performer_name:", p.performer_name)
    print("cover_ids:", p.cover_ids)
    print("work_ids:", p.work_ids)
    print("release_ids:", p.release_ids)
    print("originals:", p.originals)
    print("is_original:", p.is_original)
    print("has_spotify_link:", p.has_spotify_link)
    print("has_youtube_link:", p.has_youtube_link)
    print("youtube_url:", p.youtube_url)
    print("spotify_url:", p.spotify_url)


SHS_API_KEY = "YOUR_SHS_API_KEY"
api = Api(api_key=SHS_API_KEY)

performance_id = 290542
performance = api.get_performance(performance_id)
print_performance(performance)

```

expected result:

```
id: 290542
title: Summertime
uri: https://secondhandsongs.com/performance/290542
performer_name: Jane Powell
cover_ids: []
originals: ['4681']
is_original: False
has_spotify_link: True
has_youtube_link: True
youtube_url: https://www.youtube.com/watch?v=1me2dpYihvM
spotify_url: https://open.spotify.com/track/0lpMCyBjknQ7WHYXo4IY3P
```

The retrieved payload is available as well:

```python
  {
    'entityType': 'performance',
    'uri': 'https://secondhandsongs.com/performance/290542',
    'title': 'Summertime',
    'performer': {
      'uri': 'https://secondhandsongs.com/artist/17651',
      'name': 'Jane Powell'},
    'isOriginal': False,
    'date': None,
    'releases': [
      {'entityType': 'release',
      'entitySubType': 'album',
      'uri': 'https://secondhandsongs.com/release/100032',
      'title': 'Date with Jane Powell',
      'performer': {
        'uri': 'https://secondhandsongs.com/artist/17651',
        'name': 'Jane Powell'}
      }
    ],
    'works': [
      {'entityType': 'work',
       'entitySubType': 'song',
       'uri': 'https://secondhandsongs.com/work/4681',
       'title': 'Summertime'
      }
    ],
    'originals': [
      {'entityType': 'work',
       'entitySubType': 'song',
       'uri': 'https://secondhandsongs.com/work/4681',
       'title': 'Summertime',
       'isRootWork': True,
       'original':
        {'entityType': 'performance',
        'uri': 'https://secondhandsongs.com/performance/4681',
        'title': 'Summertime',
        'performer':
          {'uri': 'https://secondhandsongs.com/artist/2223',
           'name': 'Abbie Mitchell'
          },
          'isOriginal': True
        }
      }
    ],
    'covers': [],
    'derivedWorks': [],
    'sampledBy': [],
    'usesSamplesFrom': []
  }

```

#### Get the original performance:

```python
original_performance = performance.get_original()
print_performance(original_performance)
```

expected result:

```
id: 4681
title: Summertime
uri: https://secondhandsongs.com/performance/4681
performer_name: Abbie Mitchell
cover_ids: ['307264', '307273', ..., '1392891', '1388762']     #  (2242 records)
originals: []
is_original: True
has_spotify_link: False
has_youtube_link: False
youtube_url: None
spotify_url: None
```

#### Get the original work:
```python

print(performance.work_ids)  # => ['4681']
work = performance.get_works()[0]

def print_work(w):
    print("id:", w.id)
    print("title:", w.title)
    print("uri:", w.uri)
    print("language:", w.language)
    print("version_ids (first 5):", w.version_ids[:5])
    print("total versions:", len(w.version_ids))

print_work(work)
```

Or retrieve the work directly by the id:

```python

print(api.get_work(4681).title)  # => Summertime

```



#### Get artists
```python

print(api.get_artist(1234))

```


#### Creating datasets

**NOTE:** Youtube and Spotify links are delivered only for requests
authenticated with valid SHS api keys.


```python
from dotenv import load_dotenv
import os
from secondhandsongs import download as dl
from secondhandsongs import dataset as ds
from secondhandsongs import Api

# Set the folder where the dataset will be generated
OUTPUT_FOLDER = './output'
DATASET_FILE = './slice.csv'

# Loading the API key from an .env file using dotenv
load_dotenv()
SHS_API_KEY = os.getenv('SHS_API_KEY')
api = Api(api_key=SHS_API_KEY)


# You can set a list of stopwords
# to skip items containing these terms in the title
STOPWORDS = ['Christmas', 'Santa', 'Claus', 'Silent Night', 'God',
             'Bells', 'Nosed', 'Glory', 'Pachelbel', 'Jesus',
             'Greensleeves', 'Snowman', 'Noel', 'Noël' ]

# Build a dataset slice with 80 different works, with 4 performances per work
ds.Dataset().create_slice(DATASET_FILE, OUTPUT_FOLDER, api,
                          num_items=80,
                          cluster_size=4,
                          stopwords=STOPWORDS)

# download the performances contained in the novel dataset file
dl.yt_download(DATASET_FILE, OUTPUT_FOLDER)
```

the resulting dataset will be like this:

```
work_id,performance_id,title,url
21356,312493,The Little Drummer Boy,https://www.youtube.com/watch?v=vujkelpIfEk
21356,321027,Little Drummer Boy,https://www.youtube.com/watch?v=nk9zMGGtRC4
21356,332119,Little Drummer Boy,https://www.youtube.com/watch?v=zYkQssoj2FU
21356,341595,The Little Drummer Boy,https://www.youtube.com/watch?v=rxaTD_bHjK8
1409,323951,Yesterday,https://www.youtube.com/watch?v=dWO_HpkY-N0
1409,326659,Yesterday,https://www.youtube.com/watch?v=MaDlTw5nG7I
1409,338349,Yesterday,https://www.youtube.com/watch?v=RMh_wTZEvk8
1409,346860,Yesterday,https://www.youtube.com/watch?v=1XjU6unPID0
...

```
