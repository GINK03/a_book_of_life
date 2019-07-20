import pandas as pd
from sklearn.decomposition import NMF
import pickle
import json
import Sanitize
from scipy.sparse import lil_matrix
import numpy as np
import sys
from pathlib import Path
import re
from sklearn.metrics import mean_squared_error
if '--fit' in sys.argv:
    fnsTrain, csrTrain, fnsTest, csrTest = pickle.load(open('ser.pkl', 'rb'))
    print('fit non-negative matrix factorization')
    model = NMF(n_components=20, max_iter=600, init='random', random_state=0)
    model.fit(csrTrain)

    yhat = np.dot(model.transform(csrTest), model.components_)
    print(yhat.shape)
    mse = mean_squared_error(csrTest.todense(), yhat)
    print(f'test mse = {mse:0.06f}')
    with open('./works/models.pkl', 'wb') as fp:
        pickle.dump(model, fp)
    exit(1)
assert Path('./works/models.pkl').exists(), "there is not model."

with open('./works/models.pkl', 'rb') as fp:
    model = pickle.load(fp)
for sidx, source_json in enumerate(['./sort_source_books.json']): #, '../MakeBookReadMatrix/works/each_shelve/0000523d86c03863']):
    if sidx == 0:
        source = json.load(open(source_json))
    else:
        source = []
        for b in json.load(open(source_json))['books']:
            try:
                source.append(re.search(r'『(.*?)』', b).group(1))
            except Exception as ex:
                print(ex)
                ...

    target = json.load(open('./sort_target_books.json'))
    target_idx = {t: idx for idx, t in enumerate(target)}
    Csr = lil_matrix((1, len(target_idx)))
    for book in source:
        try:
            Csr[0, target_idx[Sanitize.sanitize(book)]] = 1
        except Exception as ex:
            print(ex)

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
    df.to_csv(f'scores_{sidx:02d}.csv', index=None)
