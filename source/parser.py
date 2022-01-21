
from parse_ingredients import parse_ingredient
from recipe_scrapers import scrape_me

def parse_recipe(url : str):
    scraper = scrape_me(url, wild_mode=True)
    recipe = {}
    ingredients = {}
    
    attributes = filter(lambda x: x != 'soup', 
                 filter(lambda x: x != 'links', 
                 filter(lambda x: not(x.startswith("__")), dir(scraper))))
    
    for att in attributes:
        try:
            recipe[att] = scraper.__getattribute__(att)()
        except:
            pass
    assert len(recipe['ingredients'])
    for ingredient in recipe['ingredients']:
        result = parse_ingredient(ingredient)
        name = result.original_string
        ingredients[name] = {}
        ingredients[name]['comment'] = result.comment
        ingredients[name]['name'] = result.name
        if not result.quantity:
            ingredients[name]['quantity']= 1
        else:
            ingredients[name]['quantity']= result.quantity
        ingredients[name]['unit']= result.unit
    
    recipe['ingredients'] = ingredients
    return recipe