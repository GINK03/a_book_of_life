import pandas as pd
from sklearn.decomposition import NMF
import pickle
import json
import Sanitize
from scipy.sparse import lil_matrix
import numpy as np
import sys
from pathlib import Path

source = json.load(open('./sort_source_books.json'))
target = json.load(open('./sort_target_books.json'))
target_idx = {t: idx for idx, t in enumerate(target)}
Csr = lil_matrix((1, len(target_idx)))
for book in source:
    try:
        Csr[0, target_idx[Sanitize.sanitize(book)]] = 1
    except Exception as ex:
        print(ex)

if '--fit' in sys.argv:
    fns, csr = pickle.load(open('ser.pkl', 'rb'))
    print('fit non-negative matrix factorization')
    model = NMF(n_components=30, init='random', random_state=0)
    model.fit(csr)
    with open('./works/models.pkl', 'wb') as fp:
        pickle.dump(model, fp)
assert Path('./works/models.pkl').exists(), "there is not model."
with open('./works/models.pkl', 'rb') as fp:
    model = pickle.load(fp)

P = model.transform(Csr)
Q = model.components_
print(len(np.dot(P, Q)[-1]))

pq = np.dot(P, Q)[-1]
idx_target = {idx: target for target, idx in target_idx.items()}
objs = []
for idx, target in idx_target.items():
    obj = {'book': target, 'score': pq[idx]}
    objs.append(obj)
df = pd.DataFrame(objs).sort_values(by=['score'], ascending=False)
df.to_csv('scores.csv', index=None)
