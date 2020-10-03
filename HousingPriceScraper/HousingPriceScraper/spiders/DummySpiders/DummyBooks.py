"""
file containing code for Dummy Books Spider. I will use this spider to test all future changes.

TODO - write method to test xpath
     - write method to test css
"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today


class DummyBooksSpider(AncestorSpider):

    name = 'dummy-books'
    input_urls = ['http://books.toscrape.com/']
    data_path = 'data/raw_data/dummy_data/{}/{}'.format(name, date_today())

    def parse(self, response):
        print('test passed dummy books')
        pass
