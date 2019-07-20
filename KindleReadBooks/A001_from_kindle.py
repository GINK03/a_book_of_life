from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
import bs4
import hashlib
from pathlib import Path
import gzip
import sys
import pickle
import time
import os
import random
from pathlib import Path
PASSWORD = os.environ['PASSWORD']
EMAIL = os.environ['EMAIL']

def random_sleep():
    time.sleep(random.random())

Path('outputs').mkdir(exist_ok=True)

def run():
    options = Options()
    Path('UserData').mkdir(exist_ok=True)
    options.add_argument('--user-data-dir=UserData')
    options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
    options.add_argument(
        "lang=ja,en-US;q=0.9,en;q=0.8")
    options.add_argument(
        "dnt=1")
    options.add_argument(
        "referer=http://www.google.com")
    desired_capabilities = DesiredCapabilities.CHROME.copy()
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path='/usr/local/bin/chromedriver',
                              desired_capabilities=desired_capabilities)
    driver.set_window_size(1080, 1080*15)
    # driver.get('https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending')
    driver.get('https://amazon.co.jp/gp/digital/fiona/manage')
    random_sleep()

    driver.save_screenshot('1.png')

    try:
        driver.find_element_by_id("ap_email").send_keys(
            EMAIL)
        driver.find_element_by_id("ap_password").send_keys(PASSWORD)
        driver.find_element_by_id("signInSubmit").click()
    except Exception as ex:
        print(ex)
    try:
        # driver.find_element_by_id("ap_email").send_keys('gim.kobayashi@gmail.com')
        driver.find_element_by_id("ap_password").send_keys(PASSWORD)
        driver.find_element_by_id("signInSubmit").click()
    except Exception as ex:
        print(ex)
    
    driver.get('https://amazon.co.jp/gp/digital/fiona/manage')
    time.sleep(5.) 
    driver.save_screenshot('2.png')
    start = time.time()
    for i in range(20):
        print(f'now iter {i} elapsed={time.time()-start}')
        random_sleep()
        start = time.time()
        wait = WebDriverWait(driver, 300)
        try:
            elm = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//div[contains(@ng-show,"paginationThresholdReached")]//button')))

            driver.save_screenshot(f'outputs/fiona_{i:02d}.png')
            html = driver.page_source
            open(f'outputs/books_{i:02d}.html', 'w').write(html)
            # driver.find_element_by_xpath('//div[contains(@ng-show,"paginationThresholdReached")]//button').click()
            elm.click()
        except Exception as ex:
            break


if __name__ == '__main__':
    run()
