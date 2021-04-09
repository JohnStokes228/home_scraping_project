"""
spider for scraping UFCstats.com. some decision will need to be made about how to do this as the data is both per
fighter and per fight...?

"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
import time
from random import randint
import scrapy


class UFCStatsBaseSpider(AncestorSpider):

    def get_items(self, response):
        pass
