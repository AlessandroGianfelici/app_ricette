import logging
import multiprocessing
import os
import sys
from datetime import datetime
from multiprocessing.dummy import Pool

import pandas as pd
from langdetect import detect

from source.constants import JSON_PATH, APP_PATH
from source.functions import read_json


def extract_ingredients(json_file):
    try:
        recipe_dict = read_json(os.path.join(JSON_PATH, json_file))
        #assert detect(recipe_dict['instructions']) == 'en', 'Only english language is supported now!'
        recipe_ingredients = list(map(lambda x : recipe_dict['ingredients'][x]['name'].lower(), 
                                      recipe_dict['ingredients'].keys()))
        df_result = pd.DataFrame()
        df_result['ingredients'] = recipe_ingredients
        df_result['url'] = recipe_dict['canonical_url']
        df_result['name'] = json_file
    except Exception as e:
        df_result = pd.DataFrame()
    return df_result

if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S%p")

    logger = logging.getLogger(__name__)

    start = datetime.now()
    pool = Pool(multiprocessing.cpu_count()-1)
    my_df = pd.concat(pool.map(extract_ingredients, os.listdir(JSON_PATH)))
    pool.close()
    logger.info(f"Parsed {len(my_df['name'].unique())} recipes in {datetime.now() - start}")
    my_df.dropna().to_parquet(os.path.join(APP_PATH, "data", "dataset.parquet"))
