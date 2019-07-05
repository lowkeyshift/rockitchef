from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://www.shopmarketbasket.com/weekly-flyer"
chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"./chromedriver")
browser.get(url)
html = browser.page_source
soup = bs(html, 'lxml')
price = soup.findAll('div', {'class': 'price-holder'})
title = soup.findAll('div', {'class': 'heading'})

onsale_dict = {}

for amount in price:
    savings = amount.find('h2').get_text()
    for item in title:
        item = item.find('h2').get_text()
        onsale_dict[item] = savings

print(onsale_dict)
