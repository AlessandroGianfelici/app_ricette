# -*- coding: utf-8 -*-
import json
import os

import numpy as np
import pandas as pd
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from source.functions import select_or_create
from source.parser import parse_recipe
from urllib.parse import urlparse

APP_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUTPATH = select_or_create(os.path.join(APP_PATH, 'data', 'json'))
URLS = list(np.squeeze(
                 pd.read_csv(
                     os.path.join(APP_PATH, "data", "supported_websites.csv"), 
                     header=None).values))

DOMAINS = list(map(lambda x : urlparse(x).netloc, URLS))

class MySpider(CrawlSpider):
    name = 'gspider'
    allowed_domains = DOMAINS
    start_urls = URLS
    rules = (# Extract and follow all links!
        Rule(LinkExtractor(), callback='parse_item', follow=True), )
               
    def parse_item(self, response):
        recipe_dict = parse_recipe(response.url)
        filename = recipe_dict['title'].replace(" ", "_")
        with open(os.path.join(OUTPUTPATH, filename), 'w') as outfile:
            json.dump(recipe_dict, outfile)
        self.log('crawling'.format(response.url))
