import requests
import json
import sqlite3
from bs4 import BeautifulSoup as bf


class AllRecipes:
    'bs4 web scraper for AllRecipes.com'

    def __init__(self, ingredients):
        self.ingredients = ingredients

    def build_url(self):
        clean_items = []
        search_term = self.ingredients.split(",")
        amount = len(search_term)
        for term in search_term:
            link_ready = term.replace(" ", "%20")
            clean_items.append(link_ready)
            words = str(clean_items).strip("[]")
            items = words.replace(" ","").replace("'", "")
        if amount == 1:
            # keyword_url i.e single keyword item to search
            url = "https://www.allrecipes.com/search/results/?wt={}&sort=re".format(items)
        else:
            # ingredients_url i.e. multiple keyword items to search
            url = "https://www.allrecipes.com/search/results/?ingIncl={}&sort=re".format(items)
        return url


    def parse_url(self,url):
        r = requests.get(url)
        soup = bf(r.text, 'html.parser')
#################ALLRECIPES INTEGRATION###############################
        # Main Recipe Title to the page <### Don't Need Anymore ###>
        main_title = soup.find(class_="recipe-summary__h1").get_text().replace('\n','')
        json_dict['recipes'].update({main_title: {}})

        # Collect Tags from html
        tags_lambda =lambda x: x and x.startswith(('toggle-similar__title'))
        tags = [x.text.replace('\n','').strip() for x in soup.findAll('span', class_=tags_lambda) if 'Recipe' not in x.text and 'Home' not in x.text]
        json_dict['recipes'][main_title].update({'tags':list(tags)})

        # All ingredients listed and looped over with only text
        # removed add all ingredients button text
        ingredients_list = []
        ingredients_scrape = soup.findAll(class_="recipe-ingred_txt")
        for ingredients in ingredients_scrape:
            ingredients_cleaned = ingredients.get_text().replace('\n', '')
            if ingredients_cleaned != "Add all ingredients to list" and ingredients_cleaned != '':
                ingredients_list.append(ingredients_cleaned)
                json_dict['recipes'][main_title].update({'ingredients':ingredients_list})

        # Collect and display recipe directions text.
        directions_list = []
        directions = soup.findAll("span", class_="recipe-directions__list--item")
        for dir in directions:
            directions_cleaned = dir.get_text().replace('\n','')
            if directions_cleaned != '':
                directions_list.append(directions_cleaned)
                json_dict['recipes'][main_title].update({'directions':directions_list})
        preptime_list = []
        # Collect specific prep,cook and ready time from directions.
        prep_time = soup.findAll("li", attrs={"aria-label":True, "class":"prepTime__item"})
        #print(directions)
        for steps in prep_time:
            preptime_list.append(steps["aria-label"])
            json_dict['recipes'][main_title].update({'prep_time':preptime_list})

my_ingredients = AllRecipes("cucumbers, peppers, chicken") ## needs to be called from a separate script that will use this class.
###Next Step is to use DB connection###
#conn = sqlite3.connect('./rockit/rockit.db')
json_dict = {'recipes':{}}

r = requests.get(my_ingredients.build_url())
soup_search = bf(r.text, 'html.parser')
link_list = soup_search.find_all('a', class_="fixed-recipe-card__title-link")
if len(link_list) == 0:
    print("0 Search Results")
else:
    for links in link_list:
        url = links.get('href')
        my_ingredients.parse_url(url)
## Remove all of the JSON and replce with DB connections.
# Keep the way its built, will come in handy when pulling from DB.
print(json.dumps(json_dict, indent=4, sort_keys=True))
