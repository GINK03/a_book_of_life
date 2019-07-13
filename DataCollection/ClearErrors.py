from pathlib import Path
import gzip
import pickle
from collections import namedtuple
HTML_TIME_ROW = namedtuple(
    'HTML_TIME_ROW', ['html', 'time', 'url', 'status_code'])
for path in Path().glob('./tmp/htmls/*'):
    data =pickle.loads(gzip.decompress(path.open('rb').read()))
    if not isinstance(data, list):
        path.unlink()
        print(type(data))
