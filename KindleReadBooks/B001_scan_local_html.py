import glob
from bs4 import BeautifulSoup as BS
import json
books = []
for fn in glob.glob('./outputs/books_*.html'):
    html = open(fn).read()
    soup = BS(html)

    for div in soup.find_all('div', {'class': 'contentTableListRow_myx'}):
        # for col in div.find_all('div', {'class':'myx-column'}):
        # print(col.text.strip(), end="|")

        bo_title = div.find('div', {'bo-text': 'tab.title'})
        bo_author = div.find('div', {'bo-text': 'tab.author'})
        bo_day = div.find('div', {'bo-text': 'tab.purchaseDate'})
        print(bo_title.text, bo_author.text, bo_day.text)
        books.append(bo_title.text)
json.dump(books, fp=open('books.json', 'w'), indent=2, ensure_ascii=False)
