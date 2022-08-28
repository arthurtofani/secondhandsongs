import os
import os.path
import pandas as pd

YTDL_URL = 'youtube-dl -x --audio-format "wav" -o %s %s'
FFMPEG_COMMAND = 'ffmpeg -i %s -acodec pcm_s16le -ac 1 -ar 22050 %s'


def yt_download(input_file, output_folder):
    invalid_list = [str(x) for x in get_invalid_list(output_folder)]
    try:
        df = pd.read_csv(input_file)
        for i, row in df.iterrows():
            fld = output_folder + '/' + str(row.work_id)
            filename = fld + '/' + str(row.performance_id) + '.wav'
            if row.performance_id in invalid_list:
                continue
            if not os.path.exists(filename):
                ret = os.system(YTDL_URL % (filename + '.wav', row.url))
                if ret != 0:
                    _save_invalid_record(output_folder, row.performance_id)
                else:
                    os.system(FFMPEG_COMMAND % (filename + '.wav', filename))
                    os.system('rm %s.wav' % filename)
            else:
                print('file %s already exists' % filename)
    except KeyboardInterrupt:
        return


def get_invalid_list(output_folder):
    file = _invalid_list_path(output_folder)
    if os.path.exists(file):
        with open(file, 'r') as f:
            lst = f.read().split('\n')[:-1]
            return lst
    else:
        return []


def _save_invalid_record(output_folder, performance_id):
    print("Performance ID [%s] - link not found", performance_id)
    with open(_invalid_list_path(output_folder), 'a') as f:
        f.write('%s\n' % performance_id)


def _invalid_list_path(output_folder):
    return output_folder + '/invalid.txt'
