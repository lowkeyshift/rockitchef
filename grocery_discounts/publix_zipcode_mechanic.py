from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import time

"""Searches Publix store nearest you and sets as store for coupons"""

url = "https://store.publix.com/publix/"
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"./chromedriver")
driver.get(url)
time.sleep(2)

# Zip Code Search
zip = 32804 # Orlando, FL Zipcode
delay = 5

try:
    # Wait for page to load
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'txtLocation')))
    text_box = driver.find_element_by_id('txtLocation') # input selector
    text_box.send_keys(zip) # enter zipcode in input
    driver.find_element_by_id('btnSearch').click() # click the submit button

    # Wait for page to load
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn.js-btnSetStore')))
    # Click on 'Make My Publix' Button
    driver.find_element_by_class_name('btn.js-btnSetStore').click()


    # BoGo page for specials; will auto generate page to location
    # Wait for page to load
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'publix-megamenu-btnSavings')))
    #hover action
    action = ActionChains(driver)
    first_lvl_dropdown_link = driver.find_element_by_link_text('Savings')
    action.move_to_element(first_lvl_dropdown_link).perform()
    print("first movement")
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'publix-megamenu-btnSavings')))
    second_lvl_dropdown_link = driver.find_element_by_link_text('Weekly BOGOs')
    print("second movement")
    action.move_to_element(second_lvl_dropdown_link).perform()
    # Click on 'Bogo dropdown' link
    second_lvl_dropdown_link.click()
    print("clicked on bogo")

    #x_path = '//*[@id="main-content"]/div[3]/div[2]/div[1]/div[1]/p[2]/a'
    # Wait for page to load
    #WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, x_path)))
    # Click on 'savings' nav Button
    #driver.find_element_by_xpath(x_path).click()

    # Should now be on the BOGO Items List page
    # Grab the current URL
    driver.implicitly_wait(2)
    bogo_page = driver.current_url
    print(bogo_page)
    bogo_html = driver.page_source

    # BS4 starts here for BOGO Deals
    soup = bs(bogo_html, 'lxml')


    #savings = soup.findAll('div', {'class': 'circle-deal'})

    onsale_dict = {}

    #title_lst_comp = [item.find('h2').get_text() for item in title]
    item_titles = soup.findAll('title') #('div', class_='gridTileUnitB gridHasCouponBtns')
    #<span class="title cursorPointer action-tracking-nav action-goto-listingdetail desktopBBDTabletTitle" data-maxrows="4">6-Pack 7UP Products</span>
    print(item_titles)
    driver.quit()
except Exception as e:
    print(e)



driver.quit()
