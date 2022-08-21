import youtube_dl
import os
import os.path
import pandas as pd

YTDL_URL = 'youtube-dl -x --audio-format "wav" -o %s %s'


def yt_download(input_file, output_folder):
  df = pd.read_csv(input_file)
  for i, row in df.iterrows():
      fld = output_folder + '/' + str(row.work_id)
      filename = fld + '/' + str(row.performance_id) + '.wav'
      if not os.path.exists(filename):
          ret = os.system(YTDL_URL % (filename + '.wav', row.url ))
          os.system('ffmpeg -i %s -acodec pcm_s16le -ac 1 -ar 22050 %s' % (filename + '.wav', filename))
          os.system('rm %s.wav' % filename)

      else:
          print('file %s already exists' % filename)

