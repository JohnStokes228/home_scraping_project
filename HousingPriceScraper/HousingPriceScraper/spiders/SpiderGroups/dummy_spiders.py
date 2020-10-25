"""
project file to group the dummy spiders together. gives an idea of how realisations of spider groups will work

TODO - probably want a better way of dealing with the saving of the data here...?
"""
from HousingPriceScraper.HousingPriceScraper.spiders.DummySpiders.DummyBooks import DummyBooksBaseSpider, DummyBookAttrSpider
from HousingPriceScraper.HousingPriceScraper.spiders.DummySpiders.DummyQuotes import DummyQuotesBaseSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today


group_path = 'data/raw_data/dummy_data/'


class DummyBooks(DummyBooksBaseSpider):

    name = 'dummy-books-items'
    data_path = '{}/{}/{}'.format(group_path, name.rsplit('-', 1)[0], date_today())


class DummyBooksAttributes(DummyBookAttrSpider):

    name = 'dummy-books-attributes'
    data_path = '{}/{}/{}'.format(group_path, name.rsplit('-', 1)[0], date_today())


class DummyBooksCombiSpider(DummyBooksBaseSpider, DummyBookAttrSpider):

    name = 'dummy-books-combi'
    data_path = '{}/{}/{}'.format(group_path, name.rsplit('-', 1)[0], date_today())


class DummyQuotes(DummyQuotesBaseSpider):

    name = 'dummy-quotes-items'
    data_path = '{}/{}/{}'.format(group_path, name.rsplit('-', 1)[0], date_today())
