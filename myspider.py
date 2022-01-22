# -*- coding: utf-8 -*-
import json
import os

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from source.constants import DOMAINS, JSON_PATH, URLS
from source.functions import select_or_create, write_json
from source.parser import parse_recipe


class MySpider(CrawlSpider):
    name = 'gspider'
    allowed_domains = DOMAINS
    start_urls = URLS
    rules = (# Extract and follow all links!
        Rule(LinkExtractor(), callback='parse_item', follow=True), )
               
    def parse_item(self, response):
        recipe_dict = parse_recipe(response.url)
        filename = recipe_dict['title'].replace(" ", "_")
        write_json(recipe_dict, 
                   os.path.join(select_or_create(JSON_PATH), 
                                filename))
        self.log('crawling'.format(response.url))
