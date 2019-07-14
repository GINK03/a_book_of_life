import glob
from bs4 import BeautifulSoup as BS
import pickle
import gzip
from collections import namedtuple
import urllib.parse
from concurrent.futures import ProcessPoolExecutor as PPE

HTML_TIME_ROW = namedtuple(
    'HTML_TIME_ROW', ['html', 'time', 'url', 'status_code'])

args = [(idx, fn) for idx, fn in enumerate(glob.glob('./tmp/htmls/*')[:100000])]

def pmap(arg):
    stacks = set()
    idx, fn = arg
    try:
        data = pickle.loads(gzip.decompress(open(fn, 'rb').read()))

        soup = BS(data[-1].html)
        for a in soup.find_all('a', {'href': True}):
            href = a.get('href')
            urlpsub = urllib.parse.urlparse(href)
            if urlpsub.netloc != '' and 'booklog' not in urlpsub.netloc:
                continue
            urlpsub = urlpsub._replace(
                scheme='https', netloc='booklog.jp')
            #print(href, urlpsub.netloc, urlpsub.geturl())
            #if urlpsub.geturl() not in stacks:
            #    print(idx, urlpsub.geturl())
            stacks.add(urlpsub.geturl())
        # print(data)
    except Exception as ex:
        print(ex)
        ...
    return (idx, stacks)

stacks = set()
with PPE(max_workers=16) as exe:
    for idx, _sta in exe.map(pmap, args):
        stacks |= _sta
        print(idx)
with open(f'tmp/snapshots/snapshot_recover.pkl', 'wb') as fp:
    fp.write(pickle.dumps(stacks))
