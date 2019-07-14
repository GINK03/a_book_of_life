import json
import glob
from scipy.sparse import lil_matrix
import Sanitize
import re
import pickle

target = json.load(open('./sort_target_books.json'))
source = json.load(open('./sort_source_books.json'))
source_idx = {s: idx for idx, s in enumerate(source)}
target_idx = {t: idx for idx, t in enumerate(target)}

files = glob.glob('./works/each_shelve/*')
Csr = lil_matrix((len(files), len(target_idx)))

fns = []
for idx, fn in enumerate(files):
    obj = json.load(open(fn))
    books = obj['books']
    # print(books)
    fns.append(fn)
    for book in books:
        try:
            book = re.search(r'『(.*?)』', book).group(1)
            Csr[idx, target_idx[Sanitize.sanitize(book)]] = 1
        except Exception as ex:
            print(idx, ex, book)

ser = pickle.dumps((fns,Csr))
with open('ser.pkl', 'wb') as fp:
    fp.write(ser)
