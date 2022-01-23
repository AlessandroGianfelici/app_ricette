# -*- coding: utf-8 -*-
import os

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from source.constants import DOMAINS, JSON_PATH, URLS
from source.functions import select_or_create, write_json
from source.parser import parse_recipe
from source.recommender import DATASET

PROCESSED_URL = DATASET['url'].values

class MySpider(CrawlSpider):
    name = 'gspider'
    allowed_domains = DOMAINS
    start_urls = URLS
    rules = (# Extract and follow all links!
        Rule(LinkExtractor(), callback='parse_item', follow=True), )
               
    def parse_item(self, response):
        """
        This method look at the link and, if it's not already processed,
        it parse the recipe and dump it into a json file.
        """
        if response.url not in PROCESSED_URL:
            recipe_dict = parse_recipe(response.url)
            filename = recipe_dict['title'].replace(" ", "_")
            write_json(recipe_dict, 
                       os.path.join(select_or_create(JSON_PATH), 
                                    filename))
            self.log('crawling'.format(response.url))
