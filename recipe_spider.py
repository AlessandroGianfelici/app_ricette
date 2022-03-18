# -*- coding: utf-8 -*-
import os

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from source.constants import DOMAINS, JSON_PATH, URLS
from source.functions import select_or_create, write_json
from source.parser import parse_recipe


try:
    from source.recommender import DATASET
    PROCESSED_URL = DATASET['url'].values
except:
    PROCESSED_URL = []

def process_page(url : str):
    recipe_dict = parse_recipe(url)
    filename = recipe_dict['title'].replace(" ", "_").replace(".", "_")
    write_json(recipe_dict, 
               os.path.join(select_or_create(JSON_PATH), 
                            filename))
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
        if (url := response.url) not in PROCESSED_URL:
            process_page(url)
            self.log('crawling'.format(response.url))
