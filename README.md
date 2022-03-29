# Recipe APP
App to suggest a recipe using a given set of ingredients.

## Requirements 
First of all, let's install the requirements:

```bash
pip install -r requirements.txt
```

## Scraping the web
Second step, we can collect the recipe data by running the spider:

```python
scrapy runspider myspider.py
```

## Building the dataset
Now we can build the dataset::

```python
python dump_dataset.py
```

## Parser
If you want just to use the parser:

```python
from recipes.parser import parse_recipe

url = <some web address with a recipe inside>
parse_recipe(url)
```

## Recommender
Last step, we can ask our recommender to provide us a list of recipe given a list of ingredients:

```python
from recipes.recommender import recommend_recipes

list_of_ingredients = ["eggs", "bacon", "black pepper"]
recommend_recipes(list_of_ingredients, max_results=5)
```

And we will obtain a dataframe containing the names and the urls of the best 'max_results' recipes given our ingredients!
