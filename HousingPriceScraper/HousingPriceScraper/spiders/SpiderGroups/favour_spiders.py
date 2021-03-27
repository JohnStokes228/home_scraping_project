"""
file containing all spiders produced as favours for others. contents currently includes:

- smash bros footage scraping spiders for will

and thats it I'm literally so selfish :O
"""
from HousingPriceScraper.HousingPriceScraper.spiders.FavourSpiders.VodsMelee import VodsMeleeBaseSpider, VodsMeleeAttrSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today


group_path = 'HousingPriceScraper/HousingPriceScraper/data/raw_data/favour_spiders/'

class VodsMelee(VodsMeleeBaseSpider):

    name = 'vods-melee-items'
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


class VodsMeleeAttributes(VodsMeleeAttrSpider):

    name = 'vods-melee-attributes'
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


class VodsMeleeCombiSpider(VodsMeleeBaseSpider, VodsMeleeAttrSpider):

    name = 'vods-melee-combi'
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
