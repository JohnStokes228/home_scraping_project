"""
project file to group the dummy spiders together. gives an idea of how realisations of spider groups will work

TODO - probably want a better way of dealing with the saving of the data here...?
     - write dynamic url generation / access method
     -
"""
from HousingPriceScraper.HousingPriceScraper.spiders.DummySpiders.DummyBooks import DummyBooksBaseSpider, DummyBookAttrSpider
from HousingPriceScraper.HousingPriceScraper.spiders.DummySpiders.DummyQuotes import DummyQuotesBaseSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today


group_path = 'data/raw_data/dummy_data/'


class DummyBooks(DummyBooksBaseSpider):

    name = 'dummy-books'
    input_urls = ['http://books.toscrape.com/']
    data_path = '{}/{}/{}'.format(group_path, name, date_today())


class DummyBooksAttributes(DummyBookAttrSpider):

    name = 'dummy-books-attributes'
    input_urls = ['http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html']
    data_path = '{}/{}/{}'.format(group_path, name, date_today())


class DummyBooksCombiSpider(DummyBooksBaseSpider, DummyBookAttrSpider):

    name = 'dummy-books-combi'
    input_urls = ['http://books.toscrape.com/']
    data_path = '{}/{}/{}'.format(group_path, name, date_today())


class DummyQuotes(DummyQuotesBaseSpider):

    name = 'dummy-quotes'
    input_urls = ['http://quotes.toscrape.com/']
    data_path = '{}/{}/{}'.format(group_path, name, date_today())
