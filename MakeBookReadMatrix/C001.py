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
size = len(files)
files_train = files[:int(0.98*size)]
files_test = files[int(0.98*size):]
CsrTrain = lil_matrix((len(files_train), len(target_idx)))
CsrTest = lil_matrix((len(files_test), len(target_idx)))


fnsTrain, fnsTest = [], []
for type, fns, Csr, files in [('train', fnsTrain, CsrTrain, files_train), ('test', fnsTest, CsrTest, files_test)]:
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

ser = pickle.dumps((fnsTrain, CsrTrain, fnsTest, CsrTest))
with open('ser.pkl', 'wb') as fp:
    fp.write(ser)
