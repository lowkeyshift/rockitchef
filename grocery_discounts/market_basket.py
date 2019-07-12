from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

url = "https://www.shopmarketbasket.com/weekly-flyer"
chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"./chromedriver")
browser.get(url)
time.sleep(5)
html = browser.page_source
soup = bs(html, 'lxml')
price = soup.findAll('div', {'class': 'price-holder'})
title = soup.findAll('div', {'class': 'heading'})
savings = soup.findAll('div', {'class': 'circle-deal'})

onsale_dict = {}

title_lst_comp = [item.find('h2').get_text() for item in title]
price_lst_comp = [amount.find('h2').get_text() for amount in price]
savings_lst_comp = [sale.find('p', class_= 'ng-binding').get_text() for sale in savings]

for item in title_lst_comp:
    for price in price_lst_comp:
        for savings in savings_lst_comp:
            onsale_dict[item] = {'sale_price': price, 'savings_amt': savings}
print(onsale_dict)
browser.quit()
