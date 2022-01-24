import os
import numpy as np
import pandas as pd
from urllib.parse import urlparse

LANGUAGE = 'ita'

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(APP_PATH, 'data', 'json')
URLS = set(np.squeeze(
                 pd.read_csv(
                     os.path.join(APP_PATH, "data", f"supported_websites_{LANGUAGE}.csv"), 
                     header=None).values))

DOMAINS = set(map(lambda x : urlparse(x).netloc, URLS))