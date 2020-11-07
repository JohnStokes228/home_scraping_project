"""
project file to group the dummy spiders together. gives an idea of how realisations of spider groups will work

TODO - find a way to make all this repeated code become generic
"""
from HousingPriceScraper.HousingPriceScraper.spiders.DummySpiders.DummyBooks import DummyBooksBaseSpider, DummyBookAttrSpider
from HousingPriceScraper.HousingPriceScraper.spiders.DummySpiders.DummyQuotes import DummyQuotesBaseSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today


group_path = 'HousingPriceScraper/HousingPriceScraper/data/raw_data/dummy_spiders/'


class DummyBooks(DummyBooksBaseSpider):

    name = 'dummy-books-items'
    item_data = []
    attribute_data = []
    requests = []
    responses = []
    scrape_log = {date_today(): {'no_length_fails': 0,
                                 'no_NULL_fails': 0,
                                 'no_runs': 0,
                                 'no_response_urls': 0,
                                 'no_request_urls': 0,
                                 'missed_urls': [],
                                 'no_pages_scraped': 0}}
    data_path = '{}/{}/{}'.format(group_path, name.rsplit('-', 1)[0], date_today())


class DummyBooksAttributes(DummyBookAttrSpider):

    name = 'dummy-books-attributes'
    item_data = []
    attribute_data = []
    requests = []
    responses = []
    scrape_log = {date_today(): {'no_length_fails': 0,
                                 'no_NULL_fails': 0,
                                 'no_runs': 0,
                                 'no_response_urls': 0,
                                 'no_request_urls': 0,
                                 'missed_urls': [],
                                 'no_pages_scraped': 0}}
    data_path = '{}/{}/{}'.format(group_path, name.rsplit('-', 1)[0], date_today())


class DummyBooksCombiSpider(DummyBooksBaseSpider, DummyBookAttrSpider):

    name = 'dummy-books-combi'
    item_data = []
    attribute_data = []
    requests = []
    responses = []
    scrape_log = {date_today(): {'no_length_fails': 0,
                                 'no_NULL_fails': 0,
                                 'no_runs': 0,
                                 'no_response_urls': 0,
                                 'no_request_urls': 0,
                                 'missed_urls': [],
                                 'no_pages_scraped': 0}}
    data_path = '{}/{}/{}'.format(group_path, name.rsplit('-', 1)[0], date_today())


class DummyQuotes(DummyQuotesBaseSpider):

    name = 'dummy-quotes-items'
    item_data = []
    attribute_data = []
    requests = []
    responses = []
    scrape_log = {date_today(): {'no_length_fails': 0,
                                 'no_NULL_fails': 0,
                                 'no_runs': 0,
                                 'no_response_urls': 0,
                                 'no_request_urls': 0,
                                 'missed_urls': [],
                                 'no_pages_scraped': 0}}
    data_path = '{}/{}/{}'.format(group_path, name.rsplit('-', 1)[0], date_today())
