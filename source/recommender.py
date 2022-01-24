import logging
import os
from datetime import datetime
import pandas as pd

logger = logging.getLogger("__main__")

DATASET = pd.read_parquet(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "dataset.parquet")).dropna()

def drop_constant_columns(dataframe):
    """
    Drops constant value columns of pandas dataframe.
    """
    return dataframe.loc[:, (dataframe != dataframe.iloc[0]).any()]

def recommend_recipes(ingredient_list, max_results=25):
    start = datetime.now()
    agg_dict = {}
    for ingredient in ingredient_list:
        DATASET[ingredient] = DATASET['ingredients'].str.contains(ingredient, case=False).astype(int)
        agg_dict[ingredient] = sum
    agg_dict['index'] = len
    logger.info(f"Scored in {datetime.now() - start}")
    result = drop_constant_columns(pd.pivot_table(DATASET.reset_index(), index=['url', 'name'], 
                                                  values=ingredient_list + ["index"], aggfunc=agg_dict)
               .reset_index().set_index(['url', 'name', "index"]).astype(bool).astype(int)
               .reset_index())

    ingredient_set = set(ingredient_list).intersection(set(result.columns))
    result['count'] = result[ingredient_set].sum(axis=1)
    return result.sort_values(by=['count', 'index'], ascending=[False, True])\
             .reset_index(drop=True).head(max_results)[['name', 'url']]


