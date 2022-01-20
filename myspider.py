# -*- coding: utf-8 -*-
import json
import os

import scrapy
from parse_ingredients import parse_ingredient
from recipe_scrapers import scrape_me
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def parse_recipe(url : str):
    scraper = scrape_me(url, wild_mode=True)
    recipe = {}
    ingredients = {}
    
    attributes = filter(lambda x: x != 'soup', 
                 filter(lambda x: x != 'links', 
                 filter(lambda x: not(x.startswith("__")), dir(scraper))))
    
    for att in attributes:
        try:
            recipe[att] = scraper.__getattribute__(att)()
        except:
            pass
    
    for ingredient in recipe['ingredients']:
        result = parse_ingredient(ingredient)
        name = result.original_string
        ingredients[name] = {}
        ingredients[name]['comment'] = result.comment
        ingredients[name]['name'] = result.name
        ingredients[name]['quantity']= result.quantity
        ingredients[name]['unit']= result.unit
    
    recipe['ingredients'] = ingredients
    return recipe

def file_folder_exists(path: str):
    """
    Return True if a file or folder exists.
    :param path: the full path to be checked
    :type path: str
    """
    try:
        os.stat(path)
        return True
    except:
        return False

def select_or_create(path: str):
    """
    Check if a folder exists. If it doesn't, it create the folder.
    :param path: path to be selected
    :type path: str
    """
    if not file_folder_exists(path):
        os.makedirs(path)
    return path

OUTPUTPATH = select_or_create('json')

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
