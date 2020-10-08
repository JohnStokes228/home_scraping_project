"""
project file to group the dummy spiders together. gives an idea of how realisations of spider groups will work

TODO - its making a folder for none for some reason... maybe I'm accidentally starting the base spiders too?
"""
from HousingPriceScraper.HousingPriceScraper.spiders.DummySpiders.DummyBooks import DummyBooksBaseSpider
from HousingPriceScraper.HousingPriceScraper.spiders.DummySpiders.DummyQuotes import DummyQuotesBaseSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today


group_path = 'data/raw_data/dummy_data/'


class DummyBooks(DummyBooksBaseSpider):

    name = 'dummy-books'
    input_urls = ['http://books.toscrape.com/']
    data_path = '{}/{}/{}'.format(group_path, name, date_today())


class DummyQuotes(DummyQuotesBaseSpider):

    name = 'dummy-quotes'
    input_urls = ['http://quotes.toscrape.com/']
    data_path = '{}/{}/{}'.format(group_path, name, date_today())
