from pathlib import Path
import gzip
import pickle
from collections import namedtuple
HTML_TIME_ROW = namedtuple(
    'HTML_TIME_ROW', ['html', 'time', 'url', 'status_code'])
for path in Path().glob('./tmp/htmls/*'):
    try:
        data = pickle.loads(gzip.decompress(path.open('rb').read()))
    except EOFError:
        path.unlink()
        continue
    except OSError:
        path.unlink()
        continue
    if isinstance(data, list):
        continue
    if isinstance(data, AttributeError):
        continue
    path.unlink()
    print(type(data))
