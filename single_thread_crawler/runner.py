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
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

BASE_URL = 'http://127.0.0.1:8000{}'
RECIPE_FORMAT= 'recipes_crawled:{}'
CHEF_FORMAT = 'chefs:{}'

UNITS = {"cup": ["cups", "cup", "c.", "c"],
         "fluid_ounce": ["fl. oz.", "fl oz", "fluid ounce", "fluid ounces"],
         "gallon": ["gal", "gal.", "gallon", "gallons"],
         "ounce": ["oz", "oz.", "ounce", "ounces"],
         "pint": ["pt", "pt.", "pint", "pints"],
         "pound": ["lb", "lb.", "pound", "pounds"],
         "quart": ["qt", "qt.", "qts", "qts.", "quart", "quarts"],
         "tablespoon": ["tbsp.", "tbsp", "T", "T.", "tablespoon", "tablespoons", "tbs.", "tbs"],
         "teaspoon": ["tsp.", "tsp", "t", "t.", "teaspoon", "teaspoons"],
         "gram": ["g", "g.", "gr", "gr.", "gram", "grams"],
         "kilogram": ["kg", "kg.", "kilogram", "kilograms"],
         "liter": ["l", "l.", "liter", "liters"],
         "milligram": ["mg", "mg.", "milligram", "milligrams"],
         "milliliter": ["ml", "ml.", "milliliter", "milliliters"],
         "pinch": ["pinch", "pinches"],
         "dash": ["dash", "dashes"],
         "touch": ["touch", "touches"],
         "handful": ["handful", "handfuls"],
         "stick": ["stick", "sticks"],
         "clove": ["cloves", "clove"],
         "can": ["cans", "can"], "large": ["large"],
         "small": ["small"],
         "scoop": ["scoop", "scoops"],
         "filets": ["filet", "filets"],
         "sprig": ["sprigs", "sprig"],
         "packages": ["package","packages"]}

MAPPER = {}
for unit in UNITS:
  for unit_example in UNITS[unit]:
    MAPPER[unit_example] = unit

# lets remove () completely in the text and ignore the inside parts
def clean_text(line):
  return re.sub(
           r"\(.*\)", 
           "", 
           line
       )

# groups arrays together
# but over built but might be useful down the line for v2+
def order_array(array):
  holder = []
  temp = {'pos' : None, 'array':[]}
  for instance in array:
    if instance[1] != temp['pos']:
      holder.append(temp)
      temp = {'pos' : instance[1], 'array':[instance[0]]}
    else:
      temp['array'].append(instance[0])
  holder.append(temp)
  return holder[1:]

# helper function  
# splits a term like 
#    "1 large egg" -> 1,     large egg
#    "1 cup flour" -> 1 cup, flour
def process_pos(array):
  if len(array) == 1:
    return None, array[0][0]
  if len(array) == 2:
    return array[0][0], array[1][0]
  else:
    pos_pieces = order_array(array)
    cds = pos_pieces[0]['array']
    first_non_number_word = pos_pieces[1]['array'][0]
    quantity = None
    if first_non_number_word in MAPPER:
      quantity = ' '.join(cds + [first_non_number_word])
      item_parts = pos_pieces[1]['array'][1:]
      for rest in pos_pieces[2:]:
        item_parts += rest['array']
    else:
      quantity = ' '.join(cds)
      item_parts = []
      for rest in pos_pieces[1:]:
        item_parts += rest['array'] 
    return quantity, ' '.join(item_parts)

# runs the process_pos for an array of units and converts into something the api accepts
def process_ingredients(ingredients):
  ingredient_tokens = [nltk.pos_tag(word_tokenize(clean_text(ingredient_text))) for ingredient_text in ingredients]
  ingredient_payload = []
  tags = []
  for x in ingredient_tokens:
    quantity, item_raw = process_pos(x)
    #account for "carrots, finely diced"
    item_array = [x.strip() for x in item_raw.split(',')]
    if len(item_array) > 1:
      tags.append(item_array[1])
    ingredient_payload.append({'item':item_array[0], 'quantity':quantity})
  return ingredient_payload, tags

''' 
 takes a directions set:
 EX: ['Heat beef according to package directions.', 'While beef is resting, heat rice as directed on package.', 'In a medium skillet, heat 2 teaspoons of oil over medium-high heat. Cook and stir mushrooms for 3 to 4 minutes; transfer to a medium bowl. Stir in 1 teaspoon barbecue sauce. Keep warm.', 'In the same skillet, heat spinach, garlic, and 1 tablespoon water for 1 minute or until spinach is bright green and reduced in size. Transfer to a serving bowl; keep warm.', 'Add remaining 1 teaspoon oil to the skillet. Cook and stir carrots and ginger over medium-high heat for 1 minute or until carrots are crisp-tender. Transfer to a serving bowl; keep warm.', 'Cut beef into smaller pieces. Divide all ingredients among 4 bowls; drizzle with additional Korean barbecue sauce.', '']
 converts to:
 [{'direction_text': 'Heat beef according to package directions.'},
 {'direction_text': 'While beef is resting, heat rice as directed on package.'},
 {'direction_text': 'In a medium skillet, heat 2 teaspoons of oil over medium-high heat.'},
 {'direction_text': 'Cook and stir mushrooms for 3 to 4 minutes; transfer to a medium bowl.'},
 {'direction_text': 'Stir in 1 teaspoon barbecue sauce.'},
 {'direction_text': 'Keep warm.'},
 {'direction_text': 'In the same skillet, heat spinach, garlic, and 1 tablespoon water for 1 minute or until spinach is bright green and reduced in size.'},
 {'direction_text': 'Transfer to a serving bowl; keep warm.'},
 {'direction_text': 'Add remaining 1 teaspoon oil to the skillet.'},
 {'direction_text': 'Cook and stir carrots and ginger over medium-high heat for 1 minute or until carrots are crisp-tender.'},
 {'direction_text': 'Transfer to a serving bowl; keep warm.'},
 {'direction_text': 'Cut beef into smaller pieces.'},
 {'direction_text': 'Divide all ingredients among 4 bowls; drizzle with additional Korean barbecue sauce.'}]
'''
def process_directions(directions):
  sentences = [sent_tokenize(direction) for direction in directions]
  response = []
  for sentence in sentences:
    response += sentence
  return [{'direction_text':resp} for resp in response]

'''
recursively crawls a page
pulls: title, author, author url
ingredients, directions

recommended urls
then recursively pulls recommended urls
'''
def crawl_page(url, r):
    recipe_page = requests.get(url)
    rsoup = bs(recipe_page.text, 'html.parser')

    recipe_title_lambda =lambda x: x and x.startswith(('recipe-main'))
    try:
        recipe_title = rsoup.find('h1', id=recipe_title_lambda).text
    except:
        logging.debug('could not find title for url: {}'.format(url))
        return
    recipe_author = rsoup.find('span', class_='submitter__name').text

    try:
        recipe_author_img_element = rsoup.find('div', class_='submitter__img').find('a')
        recipe_author_url = recipe_author_img_element.find('a')['href']
    # insert into table if chef has not been seen before
    except (TypeError, AttributeError) as e:
        recipe_author_url = ''
        logging.debug("could not find url to chef")

    recipe_author_id =  r.get(CHEF_FORMAT.format(recipe_author)) if r.exists(CHEF_FORMAT.format(recipe_author)) else None
    if recipe_author_id is None:
        payload = {
            "name": recipe_author,
            "chef_url": recipe_author_url
        }
        resp = requests.post(BASE_URL.format('/api/v1/recipes/chefs/'), json=payload)
        r.set(CHEF_FORMAT.format(recipe_author),'1')
        recipe_author_id = resp.json()['id']

    prep_time_element = rsoup.select('time[itemprop="prepTime"]')
    prep_time = 0 if len(prep_time_element) == 0 else prep_time_element[0].text

    cook_time_element = rsoup.select('time[itemprop="cookTime"]')
    cook_time = 0 if len(cook_time_element) == 0 else cook_time_element[0].text

    tags_lambda =lambda x: x and x.startswith(('toggle-similar__title'))
    tags = [x.text.replace('\n','').strip() for x in rsoup.findAll('span', class_=tags_lambda) if 'Recipe' not in x.text and 'Home' not in x.text]

    directions = process_directions([direction.text.strip() for direction in rsoup.findAll('span', class_='recipe-directions__list--item')])
    ingredients, tags_extra = process_ingredients([ingredient.text for ingredient in rsoup.findAll('span', class_='recipe-ingred_txt added')])
    recipe_payload = {
        "chef": recipe_author_id,
        "title": recipe_title,
        "recipe_url": url,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "tags": [x.strip('"') for x in tags] + tags_extra,
        "ingredients": ingredients,
        "directions": directions
    }

    recipe_post_resp = requests.post(BASE_URL.format('/api/v1/recipes/recipes/'),json=recipe_payload)
    logging.info("posted to recipes endpoint with a {} response".format(recipe_post_resp.status_code))
    r.set(RECIPE_FORMAT.format(url),'1')
    more_urls = [(url['href']) for url in rsoup.select('a[data-internal-referrer-link="similar_recipe_banner"]')]
    q = Queue(connection=r)
    for url_item in more_urls:
        if r.exists(RECIPE_FORMAT.format(url_item)):
            result = q.enqueue(parse_url, url_item)


def parse_url(url):
    
    #sleep randomly between 0 and 5 seconds to be nice on crawled site
    time.sleep(random.random() * 5)
    r = Redis(
    #     host='hostname',
    # port=port, 
    # password='password'
    )
    #check if the url has been crawled already
    if r.exists(RECIPE_FORMAT.format(url)):
        print("already crawled url: {}".format(url))
        return
    else:
        print("crawling url: {}".format(url))
        crawl_page(url, r)