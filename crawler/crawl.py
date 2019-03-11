import requests
from bs4 import BeautifulSoup as bs
import time
import sqlite3
import random
import json

def parse_url(url,conn):
    c = conn.cursor()
    #sleep randomly between 0 and 5 seconds to be nice on crawled site
    time.sleep(random.random() * 5)

    #check if the url has been crawled already
    with conn:
        c.execute("SELECT * FROM crawled WHERE url=?;",(url,))
    crawled_already = c.fetchone()
    print(crawled_already)
    # if it has not been crawled, then crawl it
    if not crawled_already:
        print("checking url:{}".format(url))
        recipe_page = requests.get(url)
        rsoup = bs(recipe_page.text, 'html.parser')

        recipe_title_lambda =lambda x: x and x.startswith(('recipe-main'))
        recipe_title = rsoup.find('h1', id=recipe_title_lambda).text
        recipe_author = rsoup.find('span', class_='submitter__name').text
        with conn:
            c.execute("SELECT id FROM users WHERE name=?",(recipe_author,))
        recipe_author_exists = c.fetchone()
        recipe_author_url = None
        #check if chef is known based on their url
        if recipe_author_exists:
            recipe_author_id = recipe_author_exists[0]
        else:
            try:
                recipe_author_img_element = rsoup.find('div', class_='submitter__img').find('a')
                recipe_author_url = recipe_author_img_element.find('a')['href']
            # insert into table if chef has not been seen before
                
            except TypeError:
                print("could not find url to chef")
            except AttributeError:
                print("could not find url to chef")
            with conn:
                c.execute("INSERT INTO users (url,name) VALUES (?,?)",(recipe_author_url,recipe_author))
            recipe_author_id = c.lastrowid 

        prep_time_element = rsoup.select('time[itemprop="prepTime"]')
        prep_time = 0 if len(prep_time_element) == 0 else prep_time_element[0].text

        cook_time_element = rsoup.select('time[itemprop="cookTime"]')
        cook_time = 0 if len(cook_time_element) == 0 else cook_time_element[0].text

        with conn:
            c.execute("INSERT INTO recipes (title, chef_id, url, prep_time, cook_time) VALUES (?,?,?,?,?)",(recipe_title,recipe_author_id,url, prep_time, cook_time))
        recipe_id = c.lastrowid
        
        directions = [direction.text for direction in rsoup.findAll('span', class_='recipe-directions__list--item')]
        with conn:
            c.execute("INSERT INTO directions_uncleaned (recipe_id, directions_json) VALUES (?,?)",(recipe_id, json.dumps(directions)))
        
        ingredients = [(recipe_id,ingredient.text) for ingredient in rsoup.findAll('span', class_='recipe-ingred_txt added')]
        with conn:
            c.executemany("INSERT INTO ingredients_uncleaned (recipe_id, ingredient_qty) VALUES (?,?)", ingredients)
        print('inserted recipe: {}'.format(recipe_title))

        with conn:
            c.execute("INSERT INTO crawled (url, source) VALUES (?,'allrecipes')",(url,))
        more_urls = [(url['href']) for url in rsoup.select('a[data-internal-referrer-link="similar_recipe_banner"]')]
        for url_item in more_urls:
            parse_url(url_item,conn)
    else:
        print("skipping url: {}".format(url))

if __name__ == '__main__':   
    conn = sqlite3.connect('/home/aznzunit/rockit.db')
    page = 0
    while True:
        # load google page, iterate across websites
        result = requests.get("https://www.google.com/search?q=site:allrecipes.com/recipe/&start={}".format(page))
        c = result.text
        soup = bs(c,"html.parser")
        samples = soup.find_all("cite")
        for sample in samples:
            url = sample.text
            parse_url(url,conn)
        page += 10
  