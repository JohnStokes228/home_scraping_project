"""
ancestor spider is the highest generation of spider involved. will contain all base methods needing to be inherited by
all the descendant spiders.
the spiders exoskeleton wraps the set of gooey interior functions into a single class

TODO - build parse method such that it allows tactility in number of sub functions scrapers iterate through
     - build start requests method such that it is easy to call with minimal effort
     - most likely need to study the existing builds here online
     - have a set of custom settings all spiders have by default
     - consider building a second ancestor for 'item level' scrapes. a nana to every grandpa
"""
import scrapy
from HousingPriceScraper.HousingPriceScraper.functions.data_management import check_make_dir, date_today
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Cephalothorax import SpiderMethods


class AncestorSpider(scrapy.Spider, SpiderMethods):

    name = None
    input_urls = []
    custom_settings = {}
    data_path = 'data/raw_data/{}/{}'.format(name, date_today())

    def start_requests(self):
        """
        takes input urls and feeds them to the parse method.

        :return: request object(object?) which calls the parse method
        """
        check_make_dir(folder=self.data_path)
        for url in self.input_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        dummy func to be overwritten in actual spiders. this function will dictate what to do once arriving at the
        response url.

        :param response: scrapy response object - a request url
        :return: scrape target url. if told to save then hopefully it'll do just that ey ;)
        """
        pass
