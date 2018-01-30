import bs4 as bs
import urllib.request
import json

link = 'http://www.food.com/recipe/french-canadian-tourtiere-107377'
source = urllib.request.urlopen(link).read()
soup = bs.BeautifulSoup(source, 'lxml')
soup.prettify('utf-8')

recipe_content=soup.find("script", {"type": "application/ld+json"})
recipe_content_text = recipe_content.get_text()
recipe_content_json_obj = json.loads(recipe_content_text)

print(recipe_content_json_obj['description'])

print("***************")

for item in recipe_content_json_obj['recipeIngredient']:
    print(item)
          
print("*******************")
    
print (recipe_content_json_obj['recipeInstructions'])


