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

    # 解析畫面
    sourceCode = BeautifulSoup(driver.page_source, 'html.parser')
    metaSection = sourceCode.select('div.r-list-container')[0]
    sections = metaSection.select('div.r-ent')
    for section in sections:
        # 抓取資料
        title = section.select('div.title')[0].text
        num = section.select('div.nrec')[0].text
        author = section.select('div.author')[0].text
        date = section.select('div.date')[0].text

        # 顯示資料
        title = title.strip()
        print(title)
        print(num)
        print(author)
        print(date)
except Exception as e:
    traceback.print_exc()
    driver.close()