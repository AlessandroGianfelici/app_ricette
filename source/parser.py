
from parse_ingredients import parse_ingredient, units
from recipe_scrapers import scrape_me
import re

# aggiungo le versioni italiane degli ingredienti
units['cucchiaio'] = ['cucchiaio', 'cucchiai', 'cucchiaio da tè', "cucchiai da tè", 'cucchiaio da tavola', 'cucchiai da tavola']
units['cucchiaino'] = ['cucchiaino', 'cucchiaini']
units['pizzico'] = ['pizzico', 'pizzichi']
units['spicchio'] = ['spicchio', 'spicchi', 'of spicchio']
units['rametto'] = ['rametto', 'rametti']
units['q.b.'] = ['q.b.', 'q.b', 'qb']
units['ciuffo'] = ['ciuffo', 'ciuffi', 'grande ciuffo', 'grandi ciuffi']
units['foglia'] = ['foglie', 'foglia', 'foglioline', 'fogliolina']
units["bicchiere"] = ["bicchieri", "bicchiere"]
units['filetto'] = ['filetti', 'filetto']
units['stecca'] = ['stecca', 'stecche']
units['mestolo'] = ['mestolo', 'mestoli']
units['tazza'] = ['tazza', 'tazze']
units['tazzina'] = ['tazzina', 'tazzine']
units['manciata'] = ['manciata', 'manciate']
units['bustina'] = ['bustina', 'bustine']
units['busta'] = ['busta', 'buste']

units['kg'].append("chilogrammo")
units['kg'].append("chilogrammi")
units['g'].append("gr")
units['g'].append("grammo")
units['g'].append("grammi")
units['l'].append("litro")
units['l'].append("litri")
units['ml'].append("millilitri")

def treat_giallo_zafferano(ingr):
    try:
        find_dig = map(lambda x : x == ':' or (x.isdigit() and (x!='0')), ingr)
        indice = list(find_dig).index(True)
        assert indice
        result = ingr[indice:].replace(",", ".") + " " + ingr[:indice]
        return result.removeprefix(":").strip().replace(".00", "")
    except:
        return ingr.replace(",", ".")


def ingredient_to_dict(parsed):
    recipe = {}
    recipe['comment'] = parsed.comment
    recipe['name'] = re.sub(r"[^a-zA-Z0'èé]", ' ', 
                          parsed.name.strip()
                                .removeprefix("di ")
                                .removeprefix("of ")
                                .removesuffix("q.b.")
                                .lower()
                                .replace(".", "")
                                .replace("amido di mais", "maizena")
                                .replace("circa", "")
                                .replace("(", "")
                                .replace(")", "")).strip()\
                                    .removeprefix("di ")\
                                    .removeprefix("da tavola")\
                                    .removeprefix("da tè")\
                                    .strip()

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
    is_giallo = ((recipe['host'] == 'ricette.giallozafferano.it') or
                 (recipe['host'] == 'cookaround.com') or
                 (recipe['host'] == 'alimentipedia.it'))

    for ingredient in recipe['ingredients']:
        name = ingredient
        ingredient = ingredient.replace("q. b.", "q.b. ")
        if is_giallo:
            ingredient = treat_giallo_zafferano(ingredient)
        result = parse_ingredient(ingredient.lower().replace("’", "'").replace(".00", ""))
        ingredients[name] = ingredient_to_dict(result)
    recipe['ingredients'] = ingredients
    return recipe