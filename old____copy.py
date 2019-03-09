import requests
import json
from bs4 import BeautifulSoup as bf

def search_type():
    json_dict = {}
    option = input("How would you like to search? (ingredient/keyword): ")
    clean_items = []
    if option == "ingredient":
        search_term = input("Enter some ingredient. (ex: item1,item2,item3...): ")
        joining = search_term.split(",")
        for term in joining:
            link_ready = term.replace(" ", "%20")
            clean_items.append(link_ready)
        list_string = str(clean_items).strip("[]")
        new_string = list_string.replace(" ","").replace("'", "")
        search_url = "https://www.allrecipes.com/search/results/?ingIncl={}&sort=re".format(new_string)
        r_search = requests.get(search_url)
        soup_search = bf(r_search.text, 'html.parser')
        link_list = soup_search.find_all('a', class_="fixed-recipe-card__title-link")
        if len(link_list) == 0:
            print("0 Search Results")
        else:
            for links in link_list:
                url = links.get('href')
                r = requests.get(url)
                soup = bf(r.text, 'html.parser')

                # Main Recipe Title to the page <### Don't Need Anymore ###>
                main_title = soup.find(class_="recipe-summary__h1").get_text().replace('\n','')
                json_dict['recipes'] = {main_title: {}}

                # All ingredients listed and looped over with only text
                # removed add all ingredients button text
                ingredients_list = []
                ingredients_scrape = soup.findAll(class_="recipe-ingred_txt")
                for ingredients in ingredients_scrape:
                    ingredients_cleaned = ingredients.get_text().replace('\n', '')
                    if ingredients_cleaned != "Add all ingredients to list" and ingredients_cleaned != '':
                        ingredients_list.append(ingredients_cleaned)
                        json_dict['recipes'][main_title]['ingredients'] = ingredients_list

                # Collect and display recipe directions text.
                directions_list = []
                directions = soup.findAll("span", class_="recipe-directions__list--item")
                for dir in directions:
                    directions_cleaned = dir.get_text().replace('\n','')
                    if directions_cleaned != '':
                        directions_list.append(directions_cleaned)
                        json_dict['recipes'][main_title]['directions'] = directions_list
                preptime_list = []
                # Collect specific prep,cook and ready time from directions.
                prep_time = soup.findAll("li", attrs={"aria-label":True, "class":"prepTime__item"})
                #print(directions)
                for steps in prep_time:
                    preptime_list.append(steps["aria-label"])
                    json_dict['recipes'][main_title]['prep_time'] = preptime_list
            print(json.dumps(json_dict, indent=4, sort_keys=True))
    else:
        search_term = input("What are you looking to cook?: ")
        search_url = "https://www.allrecipes.com/search/results/?wt={}&sort=re".format(search_term)
        r_search = requests.get(search_url)
        soup_search = bf(r_search.text, 'html.parser')
        link_list = soup_search.find_all('a', class_="fixed-recipe-card__title-link")
        for links in link_list:
            url = links.get('href')
            r = requests.get(url)
            soup = bf(r.text, 'html.parser')

            # Main Recipe Title to the page <### Don't Need Anymore ###>
            main_title = soup.find(class_="recipe-summary__h1").get_text().replace('\n','')
            print("Recipe: {}".format(main_title))

            # All ingredients listed and looped over with only text
            # removed add all ingredients button text
            ingredients_list = soup.findAll(class_="recipe-ingred_txt")
            for ingredients in ingredients_list:
                cleaned = ingredients.get_text().replace('\n', '')
                if cleaned != "Add all ingredients to list":
                    print(cleaned)

            # Collect specific prep,cook and ready time from directions.
            directions = soup.findAll("li", attrs={"aria-label":True, "class":"prepTime__item"})
            #print(directions)
            for steps in directions:
                #print(steps.get_text().replace('\n',''))
                print(steps["aria-label"]+"\n")

search_type()
