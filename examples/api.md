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
        print("originals:", p.originals)
        print("is_original:", p.is_original)
        print("has_spotify_link:", p.has_spotify_link)
        print("has_youtube_link:", p.has_youtube_link)
        print("youtube_url:", p.youtube_url)
        print("spotify_url:", p.spotify_url)


    api = Api(api_key='YOUR_SHS_API_KEY')

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

Get the original performance:

```python
original_performance = p.get_original()
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
