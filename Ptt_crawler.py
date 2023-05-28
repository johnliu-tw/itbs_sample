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

    # 解析切換頁面按鈕
    sourceCode = BeautifulSoup(driver.page_source, 'html.parser')
    button = sourceCode.select('a.btn.wide')[1]
    x = button['href'].find('x')
    dot = button['href'].find('.')

    # 設定開始爬取資料的頁面
    index = button['href'][x+1:dot]

    # 從最新往回爬，手動設定停止頁數(eg: 6210)
    for i in range(int(index)+1, 6210, -1):
        print('第 ' + str(i) + ' 頁')
        driver.get('https://www.ptt.cc/bbs/Stock/index'+str(i)+'.html')
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
            print('標題:' + title)
            print('按讚:' + num)
            print('作者:' + author)
            print('日期:' + date)
except Exception as e:
    traceback.print_exc()
    driver.close()