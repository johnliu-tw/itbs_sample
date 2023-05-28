from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup
import os
import traceback

# 開啟瀏覽器
options = Options()
service = Service(os.getcwd() + '/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

try:
    # 開啟 ptt 網頁
    driver.get('https://www.ptt.cc/bbs/Stock/index.html')

except Exception as e:
    traceback.print_exc()
    driver.close()