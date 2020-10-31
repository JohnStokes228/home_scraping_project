"""
ancestor spider is the highest generation of spider involved. will contain all base methods needing to be inherited by
all the descendant spiders.
the spiders exoskeleton wraps the set of gooey interior functions into a single class

TODO - want a method to save scraped data at set size intervals to avoid too much data stored in memory where possible
"""
import scrapy
import json
from HousingPriceScraper.HousingPriceScraper.functions.data_management import check_make_dir, date_today, save_dict_to_json, merge_dictionaries
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Abdomen import SpiderMethods
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.HiveMind import HiveMind


class AncestorSpider(scrapy.Spider, SpiderMethods, HiveMind):

    name = None
    item_data = []
    attribute_data = []
    custom_settings = {'CONCURRENT_REQUESTS': 50,
                       'COOKIES_ENABLED': False,
                       'DOWNLOAD_DELAY': 0.3,
                       'DOWNLOAD_TIMEOUT': 60,
                       'RANDOMIZE_DOWNLOAD_DELAY': True,
                       'REDIRECT_ENABLED': False,
                       'RETRY_TIMES': 5,
                       'DOWNLOADER_MIDDLEWARES': {'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
                                                  'random_useragent.RandomUserAgentMiddleware': 400},
                       'USER_AGENT_LIST': 'configs/user_agents_list.txt'
                       }
    data_path = 'data/raw_data/{}/{}'.format(name, date_today())

    def start_requests(self):
        """
        takes input urls and feeds them to the parse method.

        :return: request object(object?) which calls the parse method
        """
        meta = {'dont_redirect': True,
                'handle_httpstatus_list': [301, 302]}
        check_make_dir(folder=self.data_path)
        with open('configs/chosen_urls.json') as input_urls_json:
            urls_dict = json.load(input_urls_json)
        input_urls = urls_dict[self.name]
        for url in input_urls:
            if hasattr(self, 'traverse_site'):
                yield scrapy.Request(url=url, meta=meta, callback=self.traverse_site)
            elif hasattr(self, 'get_items'):
                yield scrapy.Request(url=url, meta=meta, callback=self.get_items)
            elif hasattr(self, 'get_attributes'):
                yield scrapy.Request(url=url, meta=meta, callback=self.get_attributes)
            else:
                print('spider {} has no valid methods of scraping!'.format(self.name))

    def validate_save_scraped_data(self, url, data_dictionary, date_vars=False, attrs=False):
        """
        checks if variable lengths match, checks if NULLs are included within data, saves accordingly.

        :param url: url scraped
        :param data_dictionary: dictionary of scraped data to be checked
        :param date_vars: boolean indicating if date variables should be included in save
        :param attrs: boolean is the data from attribute level scrape
        :return: either appends data to spiders data attribute, or saves it as a json
        """
        lengths = [len(value) for value in data_dictionary.values()]
        if len(set(lengths)) == 1:
            print('PASS: successfully scraped {} values from:\n\t{}'.format(lengths[0], url))
            for key in data_dictionary.keys():
                if None in data_dictionary[key]:
                    print('FAIL: found NoneTypeObj in variable {}'.format(key))
                    save_dict_to_json(data_dictionary, self.data_path,
                                      'NULL_FAIL_{}'.format(self.name.rsplit('-', 1)[0]), attrs=attrs,
                                      date_vars=date_vars)
                elif attrs:
                    self.attribute_data.append(data_dictionary)
                else:
                    self.item_data.append(data_dictionary)
        else:
            print('FAIL: data features mismatched variable lengths')
            save_dict_to_json(data_dictionary, self.data_path, 'MISMATCH_FAIL_{}'.format(self.name.rsplit('-', 1)[0]),
                              attrs=attrs, date_vars=date_vars)

    def close(self, reason):
        """
        method for end of scrape, closes driver if it exists and will save

        :param reason: reason for closure of spider - unused just comes in as default.
        :return: proper finish
        """
        if hasattr(self, 'driver'):
            self.driver.quit()
        if len(self.item_data) > 0:
            self.item_data = merge_dictionaries(self.item_data)
            save_dict_to_json(self.item_data, self.data_path, self.name.rsplit('-', 1)[0])
        if len(self.attribute_data) > 0:
            self.attribute_data = merge_dictionaries(self.attribute_data)
            save_dict_to_json(self.attribute_data, self.data_path, self.name.rsplit('-', 1)[0], attrs=True)


