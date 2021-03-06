from flask import Flask, jsonify, request
from recipes.parser import parse_recipe

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config["DEBUG"] = True

@app.route('/v1/parse_recipe', methods=['GET'])
def get_recipe():
    if "url" not in request.args:
        return 'url parameter is required', 400
    else:
        url = request.args.get('url', type=str)
        return jsonify(parse_recipe(url))


if __name__ == '__main__':
    app.run()
