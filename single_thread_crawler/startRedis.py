import requests
from redis import Redis
from rq import Queue

import requests
from bs4 import BeautifulSoup as bs
import random, json, time, nltk, logging
from nltk.tokenize import sent_tokenize, word_tokenize
from urllib.parse import urlparse
import re
# https://github.com/gunthercox/ChatterBot/issues/930#issuecomment-322111087
import ssl

from systemd import journal


from runner import parse_url
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('all')


BASE_URL = 'http://rockitchef.com{}'
RECIPE_FORMAT= 'recipes_crawled:{}'
CHEF_FORMAT = 'chefs:{}'
logger = logging.getLogger('start_runners')
logger.addHandler(journalHandler())
logger.setLevel(logging.DEBUG)

def init(r):
    logger.info("collecting chefs from server")
    chefs_array = requests.get(BASE_URL.format('/api/v1/recipes/chefs/')).json()
    for chef in chefs_array:
        r.set(CHEF_FORMAT.format(chef['name']),'1')
    logger.info("collecting recipes from server")
    recipes_array = requests.get(BASE_URL.format('/api/v1/recipes/recipes/')).json()
    for recipe in recipes_array:
        r.set(RECIPE_FORMAT.format(recipe['recipe_url']),'1')
    return Queue(connection=r)

if __name__ == '__main__':
    r = Redis(
    #     host='hostname',
    # port=port, 
    # password='password'
    )
    q = init(r)

    page = 0
    while True:
        # load allrecipes homepage, iterate across recipe options
        allrecipes_url = "https://www.allrecipes.com/?page=0".format(page)
        logger.debug("checking allrecipes url: {}".format(allrecipes_url))
        result = requests.get(allrecipes_url)
        c = result.text
        soup = bs(c,"html.parser")
        samples = soup.find_all("a",{"class": "fixed-recipe-card__title-link"})
        for sample in samples:
            url = sample.get('href').split('?')[0]
            if r.exists(RECIPE_FORMAT.format(url)):
                logger.debug("already grabbed url: {}".format(url))
                continue
            else:
                logger.debug("queued up url:{}".format(url))
                result = q.enqueue(parse_url, url)
            wait_time = random.random() * 5 + 10
            logger.debug("waiting {} seconds to grab url {}".format(wait_time, url))
            time.sleep(wait_time)
        page += 1