"""
ancestor spider is the highest generation of spider involved. will contain all base methods needing to be inherited by
all the descendant spiders.
the spiders exoskeleton wraps the set of gooey interior functions into a single class

TODO - rewrite start_requests so it can know which function to send requests too based on some attribute
     - **have a set of custom settings all spiders have by default**
     - consider building a second ancestor for 'item level' scrapes. a nana to every grandpa
"""
import scrapy
import json
from HousingPriceScraper.HousingPriceScraper.functions.data_management import check_make_dir, date_today
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.abdomen import SpiderMethods


class AncestorSpider(scrapy.Spider, SpiderMethods):

    name = None
    custom_settings = {}
    data_path = 'data/raw_data/{}/{}'.format(name, date_today())

    def start_requests(self):
        """
        takes input urls and feeds them to the parse method.

        :return: request object(object?) which calls the parse method
        """
        check_make_dir(folder=self.data_path)
        with open('configs/chosen_urls.json') as input_urls_json:
            urls_dict = json.load(input_urls_json)
        input_urls = urls_dict[self.name]
        for url in input_urls:
            if hasattr(self, 'traverse_site'):
                yield scrapy.Request(url=url, callback=self.traverse_site)
            elif hasattr(self, 'get_items'):
                yield scrapy.Request(url=url, callback=self.get_items)
            elif hasattr(self, 'get_attributes'):
                yield scrapy.Request(url=url, callback=self.get_attributes)
            else:
                print('spider {} has no valid methods of scraping!'.format(self.name))
