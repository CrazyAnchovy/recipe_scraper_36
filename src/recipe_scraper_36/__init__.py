import bs4 as bs
import urllib.request
import json


#base
base_of_scrape = 'http://www.food.com/topics'
source = urllib.request.urlopen(base_of_scrape).read()
soup = bs.BeautifulSoup(source, 'lxml')

base_section = soup.find("section", {"class": "letter-index"}).find_all('a') #topics a-z only
print('check')
recipe_link_list = []
unwanted_link_list = ['topic', 'ideas', 'package', 'article', 'video', 'how-to', 'user', 'collection']

def make_soup(link): #currently not called because IT WAS SLOWER WHEN I WAS USING IT!
    """passes in whatever link we're working with and makes the beautifulSoup obj out of it"""
    this = link.get('href')#get link text only
    source = urllib.request.urlopen(this).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    return soup

for link in base_section: #a-z on food.com/topics
    this = link.get('href')#get link text only
    source = urllib.request.urlopen(this).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    level_two_section = soup.find("section", {"class": "topic-index-items"}).find_all('a')#these are categories alphabetized on the topics a-z link
    #so for every letter in topic a-z, im getting every topic out
    try:
        for link in level_two_section: #every topic i.e. a/topic,topic, topic; b/topic, topic topic
            this = link.get('href')#get link text only
            source = urllib.request.urlopen(this).read()
            soup = bs.BeautifulSoup(source, 'lxml')

            recipe_level = soup.find("script", {"type": "application/ld+json"})
            json_obj = recipe_level.get_text()
            recipe_link_list_obj = json.loads(json_obj)
            for url in recipe_link_list_obj['itemListElement']:
                try:
                    if not any(unwanted_link in (url['url']) for unwanted_link in unwanted_link_list):
                        #if the link is a not a recipe, don't get it
                                                #if the link is a not a recipe, don't get it
                        print(url['url'])
                        recipe_link_list.append(url['url'])
                        source = urllib.request.urlopen(url['url']).read()
                        soup = bs.BeautifulSoup(source, 'lxml')
                        soup.prettify('utf-8')

                        recipe_content=soup.find("script", {"type": "application/ld+json"})
                        recipe_content_text = recipe_content.get_text()
                        recipe_content_json_obj = json.loads(recipe_content_text)

                        print(recipe_content_json_obj['description'])

                        print("***************")

                        for item in recipe_content_json_obj['recipeIngredient']:
                            pass
                            print(item)

                        print("*******************")

                        print (recipe_content_json_obj['recipeInstructions'])
                except:#will add exceptions later
                    pass
    except:
        pass
    try: #some of the topics have multiple pages i.e. topics/a, a/pg2; topics/b; topics/c, c/pg2, c/pg3.
        level_two_paginated = soup.find("section", {"class": "letter-index-pages"}).find_all('a')
        for link in level_two_paginated:
            #time.sleep(.125)
            this = link.get('href')
            source = urllib.request.urlopen(this).read()
            soup = bs.BeautifulSoup(source, 'lxml')
            paginated_level = soup.find("section", {"class": "topic-index-items"}).find_all('a') #this is each page of the paginated topics
            for link in paginated_level:#these are going to be each topic link in the paginated pages i.e. topics/a/pg2/topic, pg2/topic, pg2/topic
                try:
                    #time.sleep(.125)
                    this = link.get('href')
                    #print(this)#printing topics from the extra pages
                    recipe_level = soup.find("script", {"type": "application/ld+json"})
                    json_obj = recipe_level.get_text()
                    recipe_link_list_obj = json.loads(json_obj)
                    for url in recipe_link_list_obj['itemListElement']:
                        print(url['url'])
                        print("||||||||||||||||||||||||||||||||||||||||||||||||")
                        print("||||||||||||||||||||||||||||||||||||||||||||||||")
                        print("||||||||||||||||||||||||||||||||||||||||||||||||")
                        print("||||||||||||||||||||||||||||||||||||||||||||||||")
                        print("||||||||||||||||||||||||||||||||||||||||||||||||")
                        print("||||||||||||||||||||||||||||||||||||||||||||||||")
                        print("||||||||||||||||||||||||||||||||||||||||||||||||")
                        print("||||||||||||||||||||||||||||||||||||||||||||||||")
                        print("||||||||||||||||||||||||||||||||||||||||||||||||")
                        print("||||||||||||||||||||||||||||||||||||||||||||||||")

                        recipe_link_list.append(url['url'])
                except:
                    print('oops')
                    pass
    except AttributeError:#if a topic is not paginated, you would get an attribute error.
        pass
with open ('recipe_link_file.txt', 'a') as recipe_link_file:
    recipe_link_file.seek(0, 2)
    for url in recipe_link_list:
        recipe_link_file.write(url + ',')
