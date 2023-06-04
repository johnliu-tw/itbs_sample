from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup
import os
import traceback

from datetime import date
today = date.today()
# 修改日期格式
search_date = today.strftime('%m/%d')

# 開啟瀏覽器
options = Options()
service = Service(os.getcwd() + '/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

try:
  # 開啟東森網站
  driver.get('https://news.ebc.net.tw/news/living')
  sourceCode = BeautifulSoup(driver.page_source, "html.parser")

  # 爬取資料
  article_box = sourceCode.select('div.news-list-box')[0]
  articles = article_box.select('div.style1.white-box')
  for article in articles:
      date_string = article.select('span.small-gray-text')[0].text
      if search_date not in date_string:
        continue

      title = article.select('span.title')[0].text
      summary = article.select('span.summary')[0].text
      print(title)
      print(date_string)
      print(summary)

except Exception as e:
  traceback.print_exc()
  driver.close()