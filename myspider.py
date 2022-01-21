# -*- coding: utf-8 -*-
import json
import os

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from source.functions import select_or_create
from source.parser import parse_recipe

OUTPUTPATH = select_or_create('json')
#https://github.com/hhursev/recipe-scrapers
class MySpider(CrawlSpider):
    name = 'gspider'
    allowed_domains = ['themodernproper.com']
    start_urls = ['https://themodernproper.com']
    rules = (# Extract and follow all links!
        Rule(LinkExtractor(), callback='parse_item', follow=True), )
               
    def parse_item(self, response):
        recipe_dict = parse_recipe(response.url)
        filename = recipe_dict['title'].replace(" ", "_")
        with open(os.path.join(OUTPUTPATH, filename), 'w') as outfile:
            json.dump(recipe_dict, outfile)
        self.log('crawling'.format(response.url))
