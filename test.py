import requests
from bs4 import BeautifulSoup as bs
import random
import json
import time

crawled_urls = []
chefs = {}
base_url = 'http://127.0.0.1:8000{}'
# chefs_array = requests.get('http://127.0.0.1:8000/api/v1/recipes/chefs/').json()
# for chef in chefs_array:
#     chefs[chef['chef_url']] = chef['id']

def crawl_page(url):
    recipe_page = requests.get(url)
    rsoup = bs(recipe_page.text, 'html.parser')

    recipe_title_lambda =lambda x: x and x.startswith(('recipe-main'))
    recipe_title = rsoup.find('h1', id=recipe_title_lambda).text
    recipe_author = rsoup.find('span', class_='submitter__name').text
    try:
        recipe_author_img_element = rsoup.find('div', class_='submitter__img').find('a')
        recipe_author_url = recipe_author_img_element.find('a')['href']
    # insert into table if chef has not been seen before
    except (TypeError, AttributeError) as e:
        recipe_author_url = ''
        print("could not find url to chef")

    if recipe_author in chefs:
        recipe_author_id = chefs[recipe_author]
    else:
        payload = {
            "name": recipe_author,
            "chef_url": recipe_author_url
        }
        resp = requests.post(base_url.format('/api/v1/recipes/chefs/'), json=payload)
        print(resp.text)
        recipe_author_id = resp.json()['id']

    prep_time_element = rsoup.select('time[itemprop="prepTime"]')
    prep_time = 0 if len(prep_time_element) == 0 else prep_time_element[0].text

    cook_time_element = rsoup.select('time[itemprop="cookTime"]')
    cook_time = 0 if len(cook_time_element) == 0 else cook_time_element[0].text

    tags_lambda =lambda x: x and x.startswith(('toggle-similar__title'))
    tags = [x.text.replace('\n','').strip() for x in rsoup.findAll('span', class_=tags_lambda) if 'Recipe' not in x.text and 'Home' not in x.text]

    # ingredients = [(recipe_id,ingredient.text) for ingredient in rsoup.findAll('span', class_='recipe-ingred_txt added')]
    ingredients = [{'item':'apple', 'quantity':'12 oz'}]
    recipe_payload = {
        "chef": recipe_author_id,
        "title": recipe_title,
        "recipe_url": url,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "tags": tags,
        "ingredient": ingredients,
    }

    recipe_post_resp = requests.post(base_url.format('/api/v1/recipes/recipes/'),json=recipe_payload)
    recipe_id = recipe_post_resp.json()['id']


    directions = [direction.text for direction in rsoup.findAll('span', class_='recipe-directions__list--item')]

    directions_payload = {
        'recipe': recipe_id,
        'directions_json': json.dumps(directions)
    }

    directions_post_resp = requests.post(base_url.format('/api/v1/recipes/directions'), json=directions_payload)
    crawled_urls.append(url)

    more_urls = [(url['href']) for url in rsoup.select('a[data-internal-referrer-link="similar_recipe_banner"]')]
    for url_item in more_urls:
        parse_url(url_item)


def parse_url(url):
    #sleep randomly between 0 and 5 seconds to be nice on crawled site
    time.sleep(random.random() * 5)
    #check if the url has been crawled already
    if url in crawled_urls:
        print("already crawled url: {}".format(url))
        return
    else:
        print("crawling url: {}".format(url))
        crawl_page(url)

def init():
    chefs_resp = {}
    recipes_resp = []

    chefs_array = requests.get(base_url.format('/api/v1/recipes/chefs/')).json()
    for chef in chefs_array:
        chefs_resp[chef['name']] = chef['id']

    recipes_array = requests.get(base_url.format('/api/v1/recipes/recipes/')).json()
    for recipe in recipes_array:
        recipes_resp.append(recipe['recipe_url'])
    return chefs_resp, recipes_resp

if __name__ == '__main__':
    
    chefs, crawled_urls = init()

    page = 0
    while True:
        # load google page, iterate across websites
        result = requests.get("https://www.google.com/search?q=site:allrecipes.com/recipe/&start={}".format(page))
        c = result.text
        soup = bs(c,"html.parser")
        samples = soup.find_all("cite")
        for sample in samples:
            url = sample.text
            parse_url(url)
        page += 10



# data = {
#         "chef": 1,
#         "title": "Cheese Fries Delux",
#         "recipe_url": "https://allrecipes-ziquan1.com",
#         "prep_time": "20 mins",
#         "cook_time": "30 mins",
#         "tags": [],
#         "ingredient": [
#             {
#                 "id": 1,
#                 "item": "whole milk",
#                 "quantity": "8 oz"
#             },
#             {
#                 "id": 2,
#                 "item": "cheddar",
#                 "quantity": "4 oz"
#             }
#         ]
#     }
# post = requests.post('http://127.0.0.1:8000/api/v1/recipes/recipes/', json=data)
# print(post.text)
# # requests.get('')

