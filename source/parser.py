
from parse_ingredients import parse_ingredient, units
from recipe_scrapers import scrape_me
import re

# aggiungo le versioni italiane degli ingredienti
units['cucchiaio'] = ['cucchiaio', 'cucchiai']
units['cucchiaino'] = ['cucchiaino', 'cucchiaini']
units['pizzico'] = ['pizzico', 'pizzichi']
units['spicchio'] = ['spicchio', 'spicchi', 'of spicchio']
units['rametto'] = ['rametto', 'rametti']
units['q.b.'] = ['q.b.', 'q.b']
units['ciuffo'] = ['ciuffo', 'ciuffi', 'grande ciuffo', 'grandi ciuffi']
units['foglia'] = ['foglie', 'foglia', 'foglioline', 'fogliolina']
units["bicchiere"] = ["bicchieri", "bicchiere"]
units['filetto'] = ['filetti', 'filetto']
units['stecca'] = ['stecca', 'stecche']
units['kg'].append("chilogrammo")
units['kg'].append("chilogrammi")
units['g'].append("gr")
units['g'].append("grammo")
units['g'].append("grammi")
units['l'].append("litri")
units['ml'].append("millilitri")

def treat_giallo_zafferano(ingr):
    try:
        find_dig = map(lambda x : x.isdigit(), ingr)
        indice = list(find_dig).index(True)
        assert indice
        return ingr[indice:].replace(",", ".") + " " + ingr[:indice]
    except:
        return ingr.replace(",", ".")


def ingredient_to_dict(parsed):
    recipe = {}
    recipe['comment'] = parsed.comment
    recipe['name'] = re.sub(r"[^a-zA-Z0-9']", ' ', 
                          parsed.name.strip()
                                .removeprefix("di ")
                                .removeprefix("of ")
                                .removesuffix("q.b.")
                                .lower()
                                .replace(".", "")
                                .replace("amido di mais", "maizena")
                                .replace("circa", "")
                                .replace("(", "")
                                .replace(")", "")).strip().removeprefix("di ")

    recipe['quantity'] = parsed.quantity or 1
    recipe['unit'] = parsed.unit
    return recipe

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
    is_giallo = (recipe['host'] == 'ricette.giallozafferano.it')

    for ingredient in recipe['ingredients']:
        name = ingredient
        if is_giallo:
            ingredient = treat_giallo_zafferano(ingredient)
        result = parse_ingredient(ingredient.lower().replace("’", "'"))
        ingredients[name] = ingredient_to_dict(result)
    recipe['ingredients'] = ingredients
    return recipe