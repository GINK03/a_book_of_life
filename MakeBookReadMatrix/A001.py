from pathlib import Path
import glob
import gzip
import pickle
import re
from collections import namedtuple
from concurrent.futures import ProcessPoolExecutor as PPE
from bs4 import BeautifulSoup as BS
import json
HTML_TIME_ROW = namedtuple(
    'HTML_TIME_ROW', ['html', 'time', 'url', 'status_code'])

args = [(idx, fn) for idx, fn in enumerate(
    glob.glob('../DataCollection/tmp/htmls/*'))]
Path('works/each_shelve').mkdir(exist_ok=True, parents=True)


def pmap(arg):
    stacks = set()
    idx, fn = arg
    try:
        data = pickle.loads(gzip.decompress(open(fn, 'rb').read()))
        # soup = BS(data[-1].html)
        url = data[-1].url
        if not re.search(r'(https://booklog.jp/users/[a-zA-Z0-9]{1,}$)', url):
            return None
        soup = BS(data[-1].html)
        num = soup.find('ul', {'class': 'user-activity'}
                        ).find('dd').text.strip()
        print(url, num)
        obj = {'url': url, 'num': num}
        books = []
        for idx, a in enumerate(soup.find_all('div', {'class': 'item-area'})):
            print(idx, a.find('div', {'class': 'item-area-img'}).get('title'))
            books.append(a.find('div', {'class': 'item-area-img'}).get('title'))
        obj['books'] = books
        last_fn  =fn.split('/')[-1]
        json.dump(obj, open(f'works/each_shelve/{last_fn}', 'w'), indent=2, ensure_ascii=False)
    except Exception as ex:
        print(ex)
        # ...
        Path(fn).unlink()
    return idx


with PPE(max_workers=16) as exe:
    exe.map(pmap, args)
