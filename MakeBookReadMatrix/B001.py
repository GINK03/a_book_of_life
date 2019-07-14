import glob
import json
import Sanitize
import re


if __name__ == '__main__':
    # jibun books
    books = json.load(open('../KindleReadBooks/books.json'))
    jbooks = set()
    for b in books:
        jbooks.add(sanitize(b))
    jbooks = sorted(list(jbooks))
    json.dump(jbooks, fp=open('sort_source_books.json', 'w'),
              indent=2, ensure_ascii=False)

    jbooks = set()
    print(len(jbooks))
    for fn in glob.glob('./works/each_shelve/*'):
        obj = json.load(open(fn))
        url = obj['url']
        for b in obj['books']:
            try:
                name = re.search(r'『(.*?)』', b).group(1)
            except:
                continue
            name = Sanitize.sanitize(name)
            if name not in jbooks:
                print(name)
                jbooks.add(name)
    jbooks = sorted(list(jbooks))
    json.dump(jbooks, fp=open('sort_target_books.json', 'w'),
              indent=2, ensure_ascii=False)
