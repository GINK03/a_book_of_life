import itertools
import random
import requests
import re
from bs4 import BeautifulSoup
from hashlib import sha256
from FFDB import FFDB
import urllib.parse
import datetime
from concurrent.futures import ProcessPoolExecutor as PPE
from concurrent.futures import ThreadPoolExecutor as TPE
import pickle
import glob
from pathlib import Path
import time
import os
from collections import namedtuple
import urllib.request
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities


ffdb = FFDB(tar_path='tmp/htmls')
DELAY_TIME = float(os.environ['DELAY_TIME']) if os.environ.get(
    'DELAY_TIME') else 0.0
HOSTNAME = socket.gethostname()
CPU_SIZE = int(os.environ['CPU_SIZE']) if os.environ.get('CPU_SIZE') else 16

HTML_TIME_ROW = namedtuple(
    'HTML_TIME_ROW', ['html', 'time', 'url', 'status_code'])


def scrape(arg):
    key, urls = arg
    options = Options()
    Path(
        f'works/UserData_{HOSTNAME}_{key:02d}').mkdir(exist_ok=True, parents=True)
    options.add_argument(
        f'--user-data-dir=works/UserData_{HOSTNAME}_{key:02d}')
    options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
    options.add_argument(
        "lang=ja,en-US;q=0.9,en;q=0.8")
    options.add_argument(
        "dnt=1")
    options.add_argument(
        "referer=http://www.google.com")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    desired_capabilities = DesiredCapabilities.CHROME.copy()
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path='/usr/local/bin/chromedriver',
                              desired_capabilities=desired_capabilities)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(60)
    driver.set_window_size(1080*3, 1080*6)
    ret = set()
    for url in urls:
        try:
            if not re.search('^https://booklog.jp', url):
                continue
            '''
            # i 詳細レビューはスキップ
            if re.search(r'(https://booklog.jp/users/[a-zA-Z0-9]{1,}/archives.*?$)', url):
                continue
            if re.search(r'(https://booklog.jp/item/.*?$)', url):
                continue
            if not re.search(r'(https://booklog.jp/users/[a-zA-Z0-9]{1,}$)', url):
                continue
            '''
            start_time = time.time()
            if ffdb.exists(url) is True:
                continue
            urlp = urllib.parse.urlparse(url)
            scheme, netloc = (urlp.scheme, urlp.netloc)
            driver.get(url)
            if re.search(r'(https://booklog.jp/users/[a-zA-Z0-9]{1,}$)', url):
                time.sleep(8.0)
            html = driver.page_source

            status_code = 200
            soup = BeautifulSoup(html, features='lxml')
            if 'サーバーエラーが発生しました' in str(soup.title):
                continue

            ffdb.save(key=url, val=[HTML_TIME_ROW(
                html=html, time=datetime.datetime.now(), url=url, status_code=status_code)])

            for href in set([a.get('href') for a in soup.find_all('a', {'href': True})]):
                # print(href)
                urlpsub = urllib.parse.urlparse(href)
                try:
                    if urlpsub.netloc == '':
                        urlpsub = urlpsub._replace(
                            scheme=scheme, netloc=netloc)
                    if urlpsub.scheme == '':
                        urlpsub = urlpsub._replace(scheme=scheme)
                    #urlpsub = urlpsub._replace(query='')
                except Exception as ex:
                    print(ex)
                    continue
                ret.add(urlpsub.geturl())

            time.sleep(DELAY_TIME)
            print(f'done@{key:03d}', url, str(soup.title),
                  f'elapsed={time.time() - start_time:0.04f}')
        except Exception as ex:
            print('err', url, ex)
            try:
                ffdb.save(key=url, val=ex)
            except Exception as ex:
                continue
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('finish batch-forked iteration.')
    Path('tmp/snapshots').mkdir(exist_ok=True, parents=True)
    with open(f'tmp/snapshots/snapshot_{now}.pkl', 'wb') as fp:
        fp.write(pickle.dumps(ret))
    return ret


def chunk_urls(urls):
    args = {}
    # あまり引数が多いと、メモリに乗らない
    urls = list(urls)
    random.shuffle(urls)
    #urls = urls[:300000]
    CHUNK = max([100, CPU_SIZE, 1])
    for idx, url in enumerate(urls):
        key = idx % CHUNK
        if args.get(key) is None:
            args[key] = []
        args[key].append(url)
    args = [(key, urls) for key, urls in args.items()]
    return args


def main():
    urls = set()
    urls |= scrape(
        (3, ['https://booklog.jp/item/1/4150313555']))
    print(urls)
    snapshots = sorted(glob.glob('tmp/snapshots/*'))
    for snapshot in snapshots:
        try:
            urls |= pickle.loads(open(snapshot, 'rb').read())
        except EOFError as ex:
            continue
    while True:
        urltmp = set()
        with PPE(max_workers=CPU_SIZE) as exe:
            for _urlret in exe.map(scrape, chunk_urls(urls)):
                if _urlret is not None:
                    urltmp |= _urlret
        urls = urltmp
        if len(urls) == 0:
            break


if __name__ == '__main__':
    main()
