from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup
import os
import traceback

from datetime import date
today = date.today()
# 修改日期格式
search_date = today.strftime('%Y-%m-%d')

# 開啟瀏覽器
options = Options()
service = Service(os.getcwd() + '/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

try:
  # 開啟東森網站
  driver.get('https://news.ebc.net.tw/news/living')
  sourceCode = BeautifulSoup(driver.page_source, "html.parser")

except Exception as e:
  traceback.print_exc()
  driver.close()