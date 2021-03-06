from flask import Flask, jsonify, request
from flask import redirect, url_for

from recipes.recommender import recommend_recipes
import re

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config["DEBUG"] = False

def preprocess_query(query : str):
    """
    Utility function to remove invalid
    characters from the query.
    """
    preproc = re.sub(r'[^a-zA-Z]', ' ', query).strip().replace("_", " ")
    if (len(preproc) < 3):
        return preproc
    elif preproc[:-1] == 'peperon' or preproc[:-1] == 'zucc':
        return preproc
    else:
        #stemming artigianale
        return preproc[:-1]


@app.route('/')
def index():
    return redirect(url_for('suggest_recipe'))

@app.route('/v1/suggest_recipe', methods=['GET'])
def suggest_recipe():
    if "ingredients" not in request.args:
        return 'ingredients parameter is required', 400
    else:
        max_results = request.args.get('limit', type=int, default=5)
        ingredients = request.args.get('ingredients', type=str).lower()\
                                  .replace("peperone", 'peperoni')\
                                  .replace("peperoni", 'peperone, peperoni')
        ingredient_list = list(map(preprocess_query, 
                                   ingredients.split(",")))
        suggestions = recommend_recipes(ingredient_list, max_results=max_results)
        return jsonify({"status" : "ok",
                        "ingredients" : ingredient_list,
                        "recipe_name": list(map(lambda x: x.replace("_", " "), suggestions['name'].values)),
                        "recipe_url": list(suggestions['url'].values)})


if __name__ == '__main__':
    app.run()
