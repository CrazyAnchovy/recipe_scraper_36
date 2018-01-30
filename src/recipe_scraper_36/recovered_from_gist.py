
import bs4 as bs
import urllib.request
import json

#base
base_of_scrape = 'http://www.food.com/topics'
source = urllib.request.urlopen(base_of_scrape).read()
soup = bs.BeautifulSoup(source, 'lxml')

base_section = soup.find("section", {"class": "letter-index"}).find_all('a') #topics a-z only
recipe_link_list = []
unwanted_link_list = ['topic', 'ideas', 'package', 'article', 'video', 'how-to', 'user', 'collection']

def make_soup(link):
    """passes in whatever link we're working with and makes the beautifulSoup obj out of it"""
    this = link.get('href')#get link text only
    source = urllib.request.urlopen(this).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    return soup
def make_json_obj():
    pass

for link in base_section: #a-z on food.com/topics
    make_soup(link)
    level_two_section = soup.find("section", {"class": "topic-index-items"}).find_all('a')#these are categories alphabetized on the topics a-z
    try:
        for link in level_two_section: #every topic i.e. a/topic,topic, topic; b/topic, topic topic
            make_soup(link)
            
            recipe_level = soup.find("script", {"type": "application/ld+json"})
            json_obj = recipe_level.get_text()
            recipe_link_list_obj = json.loads(json_obj)
            for url in recipe_link_list_obj['itemListElement']:
                try:
                    for link in unwanted_link_list:
                        if link in url:
                            pass
                    #if the link is a not a recipe, don't get it
                    else:
                        print(url['url'])
                        recipe_link_list.append(url['url'])
                        print(len(recipe_link_list))
                except:
                    pass
    except:
        pass
    try: #some of the topics have multiple pages i.e. topics/a, a/pg2; topics/b; topics/c, c/pg2, c/pg3. 
        level_two_paginated = soup.find("section", {"class": "letter-index-pages"}).find_all('a')     
        for link in level_two_paginated:
            #time.sleep(.125)
            make_soup(link)
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
                        recipe_link_list.append(url['url'])
                        print(len(recipe_link_list))
                except:
                    pass
    except AttributeError:#if a topic is not paginated, you would get an attribute error.
        pass
with open ('recipe_link_file.txt', 'a') as recipe_link_file:
    recipe_link_file.seek(0, 2)
    for url in recipe_link_list:
        recipe_link_file.write(url + ',')
                 
################
