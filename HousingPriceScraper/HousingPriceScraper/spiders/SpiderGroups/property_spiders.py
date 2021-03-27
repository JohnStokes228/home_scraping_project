"""
project file to group the property spiders together.

"""
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today
from HousingPriceScraper.HousingPriceScraper.spiders.PropertySpiders.FoyWilliams import FoyWilliamsBaseSpider


group_path = 'HousingPriceScraper/HousingPriceScraper/data/raw_data/property_spiders/'


class FoyWilliams(FoyWilliamsBaseSpider):

    name = 'foy-williams-items'
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