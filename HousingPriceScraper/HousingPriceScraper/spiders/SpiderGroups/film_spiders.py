"""
project file for criterion data spider

"""
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today
from HousingPriceScraper.HousingPriceScraper.spiders.FilmSpiders.CriterionCollection import CriterionCollectionBaseSpider


group_path = 'HousingPriceScraper/HousingPriceScraper/data/raw_data/criterion_spiders/'


class CriterionCollectionItems(CriterionCollectionBaseSpider):

    name = 'criterion-collection-items'
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