from flask import Flask, jsonify, request
from source.recommender import recommend_recipes
import re

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config["DEBUG"] = True

def preprocess_query(query : str):
    return re.sub(r'[^a-zA-Z]', ' ', query).strip().replace("_", " ")

@app.route('/v1/suggest_recipe', methods=['GET'])
def suggest_recipe():
    if "ingredients" not in request.args:
        return 'url parameter is required', 400
    else:
        if "limit" not in request.args:
            max_results = 5
        else:
            max_results = request.args.get('limit', type=int)
        ingredients = request.args.get('ingredients', type=str)
        ingredient_list = list(map(preprocess_query, 
                                   ingredients.split(",")))
        suggestions = recommend_recipes(ingredient_list, max_results=max_results)
        return jsonify({"status" : "ok",
                        "ingredients" : ingredient_list,
                        "recipe_name": list(map(lambda x: x.replace("_", " "), suggestions['name'].values)),
                        "recipe_url": list(suggestions['url'].values)})


if __name__ == '__main__':
    app.run()
