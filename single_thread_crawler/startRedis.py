import requests
from redis import Redis
from rq import Queue

import requests
from bs4 import BeautifulSoup as bs
import random
import json
import time
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
# https://github.com/gunthercox/ChatterBot/issues/930#issuecomment-322111087
import ssl

from runner import parse_url
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('all')

BASE_URL = 'http://127.0.0.1:8000{}'
RECIPE_FORMAT= 'recipes_crawled:{}'
CHEF_FORMAT = 'chefs:{}'


def init():
    r = Redis(
    #     host='hostname',
    # port=port, 
    # password='password'
    )
    print("collecting chefs from server")
    chefs_array = requests.get(BASE_URL.format('/api/v1/recipes/chefs/')).json()
    for chef in chefs_array:
        r.set(CHEF_FORMAT.format(chef['name']),'1')
    print("collecting recipes from server")
    recipes_array = requests.get(BASE_URL.format('/api/v1/recipes/recipes/')).json()
    for recipe in recipes_array:
        r.set(RECIPE_FORMAT.format(recipe['recipe_url']),'1')
    return Queue(connection=r)

if __name__ == '__main__':
    q = init()

    page = 0
    while True:
        # load google page, iterate across websites
        result = requests.get("https://www.google.com/search?q=site:allrecipes.com/recipe/&start={}".format(page))
        c = result.text
        soup = bs(c,"html.parser")
        samples = soup.find_all("cite")
        for sample in samples:
            time.sleep(random.random() * 5 + 10)
            url = sample.text
            print("queued up url:{}".format(url))
            result = q.enqueue(parse_url, url)
        page += 10