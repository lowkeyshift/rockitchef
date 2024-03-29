## todo
'''
move to redis + refactor crawler
move ingredient adjetives to tags -- seeded and native
'''

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

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('all')
## move to redis
crawled_urls = []
chefs = {}
base_url = 'http://127.0.0.1:8000{}'
# chefs_array = requests.get('http://127.0.0.1:8000/api/v1/recipes/chefs/').json()
# for chef in chefs_array:
#     chefs[chef['chef_url']] = chef['id']

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
    return None, array[0]
  if len(array) == 2:
    return array[0], array[1]
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
  return [{'item':process_pos(x)[1], 'quantity':process_pos(x)[0]} for x in ingredient_tokens]

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
def crawl_page(url):
    recipe_page = requests.get(url)
    rsoup = bs(recipe_page.text, 'html.parser')


    recipe_title_lambda =lambda x: x and x.startswith(('recipe-main'))
    try:
        recipe_title = rsoup.find('h1', id=recipe_title_lambda).text
    except:
        print('could not find title for url: {}'.format(url))
        return
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
        recipe_author_id = resp.json()['id']

    prep_time_element = rsoup.select('time[itemprop="prepTime"]')
    prep_time = 0 if len(prep_time_element) == 0 else prep_time_element[0].text

    cook_time_element = rsoup.select('time[itemprop="cookTime"]')
    cook_time = 0 if len(cook_time_element) == 0 else cook_time_element[0].text

    tags_lambda =lambda x: x and x.startswith(('toggle-similar__title'))
    tags = [x.text.replace('\n','').strip() for x in rsoup.findAll('span', class_=tags_lambda) if 'Recipe' not in x.text and 'Home' not in x.text]

    directions = process_directions([direction.text.strip() for direction in rsoup.findAll('span', class_='recipe-directions__list--item')])
    ingredients = process_ingredients([ingredient.text for ingredient in rsoup.findAll('span', class_='recipe-ingred_txt added')])
    recipe_payload = {
        "chef": recipe_author_id,
        "title": recipe_title,
        "recipe_url": url,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "tags": tags,
        "ingredients": ingredients,
        "directions": directions
    }

    recipe_post_resp = requests.post(base_url.format('/api/v1/recipes/recipes/'),json=recipe_payload)
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
    print("collecting chefs from server")
    chefs_array = requests.get(base_url.format('/api/v1/recipes/chefs/')).json()
    for chef in chefs_array:
        chefs_resp[chef['name']] = chef['id']
    print("collecting recipes from server")
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

