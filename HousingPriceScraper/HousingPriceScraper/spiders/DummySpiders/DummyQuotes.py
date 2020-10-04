"""
file containing Dummy Quotes spider. I will test all future changes on this spider.

TODO - write method to test xpath
     - write method to test css
"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today


class DummyQuotesSpider(AncestorSpider):

    name = 'dummy-quotes'
    input_urls = ['http://quotes.toscrape.com/']
    data_path = 'data/raw_data/dummy_data/{}/{}'.format(name, date_today())

    def parse(self, response):

        pass
