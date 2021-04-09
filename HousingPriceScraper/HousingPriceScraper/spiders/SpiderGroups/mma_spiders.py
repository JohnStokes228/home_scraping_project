"""
contains all mma related spiders, currently including:

- ufcstats
- sherdog
- wikipedia
"""
from HousingPriceScraper.HousingPriceScraper.spiders.MMASpiders.Sherdog import SherdogBaseSpider
from HousingPriceScraper.HousingPriceScraper.spiders.MMASpiders.UFCStats import UFCStatsBaseSpider
from HousingPriceScraper.HousingPriceScraper.spiders.MMASpiders.Wikipedia import (
    WikipediaCampBaseSpider,
    WikipediaFighterBaseSpider
)
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today


group_path = 'HousingPriceScraper/HousingPriceScraper/data/raw_data/mma_spiders/'


class WikipediaCampItems(WikipediaCampBaseSpider):

    name = 'wikipedia-camp-items'
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


class WikipediaFigherItems(WikipediaFighterBaseSpider):

    name = 'wikipedia-fighter-items'
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


class SherdogItems(SherdogBaseSpider):

    name = 'sherdog-items'
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


class UFCStatsItems(UFCStatsBaseSpider):

    name = 'ufc-stats-items'
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
