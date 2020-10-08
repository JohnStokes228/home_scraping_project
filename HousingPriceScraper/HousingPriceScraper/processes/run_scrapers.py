"""
file containing code to run spiders, called from main.py if run_scrape is selected.

TODO - write method to get list of spiders: basically done, though there'll need to be some further work here to filter
       it all down once we know the extent of what isn't a spider in this project
     - incorporate the menus to allow user to manually reduce the list of spiders.
     - add menu to allow user to specify configuration of input urls
     - write multiprocessing implementation - crochet/pathos worked before but is there a more elegant solution?
     - !!import spider settings for use in crawler process!!
"""
import inspect
from scrapy.crawler import CrawlerProcess
from HousingPriceScraper.HousingPriceScraper.functions.menus import end_process, basic_menu, select_spiders
from HousingPriceScraper.HousingPriceScraper.spiders.SpiderGroups.dummy_spiders import *


def set_config():
    """
    function to select which config file to utilise during the next scrape, else default to 'default' config

    :return:
    """
    print('feature not yet available')
    return True


def choose_visible_projects():
    """
    function to select which spiders are visible in the run_scrape menu to pick from,
    just used for housekeeping

    :return:
    """
    print('feature not yet available')
    return True


def simultaneous_run(list_of_spiders):
    """
    function for simultaneous running of multiple spiders.

    :param list_of_spiders: list of class objects who inherit the scrapy methods to be run
    :return: runs the scrapers
    """
    process = CrawlerProcess()
    for spider in list_of_spiders:
        process.crawl(spider)
    process.start()
    end_process()


def run_scrapers():
    """
    function to run scraping pipeline. will collate all read in spiders into a list and send it off to the reactor

    :return: will either run the scrapers, or will allow user to paginate back to main menu.
    """
    spiders_lst = [obj for obj in globals().values() if inspect.isclass(obj) and str(obj).split('.')[2] == 'spiders' and 'BaseSpider' not in str(obj)]
    spiders_lst = select_spiders(spiders_lst, ['dummy_spiders'])
    if spiders_lst == False:
        return True
    else:
        simultaneous_run(spiders_lst)


def scrape_menu():
    """
    function to interface with scrapers themselves.

    :return: takes you through the scraping menu with the #bois
    """
    options_dict = {'run_scrape': run_scrapers,
                    'set_config': set_config,
                    'choose_visible_projects': choose_visible_projects}
    basic_menu(options_dict, back=True)
    return True
