import os
import numpy as np
import pandas as pd
from urllib.parse import urlparse


APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(APP_PATH, 'data', 'json')
URLS = list(np.squeeze(
                 pd.read_csv(
                     os.path.join(APP_PATH, "data", "supported_websites.csv"), 
                     header=None).values))

DOMAINS = list(map(lambda x : urlparse(x).netloc, URLS))