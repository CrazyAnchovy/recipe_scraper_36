import bs4 as bs
import urllib.request


link = 'http://www.food.com/topics/s'


source = urllib.request.urlopen(link).read()
soup = bs.BeautifulSoup(source, 'lxml')
level_two_section = soup.find("section", {"class": "topic-index-items"}).find_all('a')
level_two_paginated = soup.find("section", {"class": "letter-index-pages"}).find_all('a') #this is the active line right now

#print(soup.prettify())

def_scrape()
for link in level_two_section:
    link = link.get('href')
    print(link)
for link in level_two_paginated: #working to get the paginations
    this = link.get('href')
    print(this)