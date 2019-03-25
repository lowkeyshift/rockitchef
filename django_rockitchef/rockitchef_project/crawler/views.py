from django.shortcuts import render

# Create your views here.

class IngredientView(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer


def StartCrawler(request):
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
    return


def get_author_json(recipe_author):
    # make api call to other viewer
    # returns the json representing the chef
    return {
        'chef' : 'chef a',
        'url' : 'www.google.com'
    }

def addchef(recipe_author_url,recipe_author):
    # add the chef
    recipe_author_id = 5
    return recipe_author_id

def getchef():
    pass

def add_directions(recipe_id, json.dumps(directions)):
    pass
    # return directions_id

def add_ingredients(ingredients):
    pass
    # return ingredients_id

def confirm_crawled(url):
    pass
    #return True

def parse_url(url):
    #sleep randomly between 0 and 5 seconds to be nice on crawled site
    time.sleep(random.random() * 5)

    #check if the url has been crawled already
    with conn:
        c.execute("SELECT * FROM crawled WHERE url=?;",(url,))
    crawled_already = c.fetchone()
    if not crawled_already:
        print("checking url:{}".format(url))
        # try:
        crawl_page(url)

    else:
        print("skipping url: {}".format(url))

def crawl_page(url):
    recipe_page = requests.get(url)
    rsoup = bs(recipe_page.text, 'html.parser')

    recipe_title_lambda =lambda x: x and x.startswith(('recipe-main'))
    recipe_title = rsoup.find('h1', id=recipe_title_lambda).text
    recipe_author = rsoup.find('span', class_='submitter__name').text
    recipe_author_exists = get_author_json(recipe_author)

    recipe_author_url = None
    #check if chef is known based on their url
    if recipe_author_exists:
        recipe_author_id = recipe_author_exists[0]
    else:
        try:
            recipe_author_img_element = rsoup.find('div', class_='submitter__img').find('a')
            recipe_author_url = recipe_author_img_element.find('a')['href']
        except (TypeError, AttributeError) as e:
            print("could not find url to chef")
        recipe_author_id = add_chef(recipe_author_url,recipe_author)

    prep_time_element = rsoup.select('time[itemprop="prepTime"]')
    prep_time = 0 if len(prep_time_element) == 0 else prep_time_element[0].text
    cook_time_element = rsoup.select('time[itemprop="cookTime"]')
    cook_time = 0 if len(cook_time_element) == 0 else cook_time_element[0].text
    tags_lambda =lambda x: x and x.startswith(('toggle-similar__title'))
    tags = [x.text.replace('\n','').strip() for x in rsoup.findAll('span', class_=tags_lambda) if 'Recipe' not in x.text and 'Home' not in x.text]
    recipe_id = add_recipe(recipe_title,recipe_author_id,url, prep_time, cook_time,','.join(tags))

    directions = [direction.text for direction in rsoup.findAll('span', class_='recipe-directions__list--item')]
    directions_id = add_directions(recipe_id, json.dumps(directions))
    ingredients = [(recipe_id,ingredient.text) for ingredient in rsoup.findAll('span', class_='recipe-ingred_txt added')]
    
    ingredients_id = add_ingredients(ingredients)
    print('inserted recipe: {}'.format(recipe_title))
    crawled = confirm_crawled(url)

    more_urls = [(url['href']) for url in rsoup.select('a[data-internal-referrer-link="similar_recipe_banner"]')]

    for url_item in more_urls:
        parse_url(url_item)

#########################################