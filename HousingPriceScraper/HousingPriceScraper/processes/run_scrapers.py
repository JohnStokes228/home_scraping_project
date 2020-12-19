"""
file containing code to run spiders, called from main.py if run_scrape is selected.

TODO - write multiprocessing implementation - crochet/pathos worked before but is there a more elegant solution?
"""
import inspect
import os
from scrapy.crawler import CrawlerProcess
from HousingPriceScraper.HousingPriceScraper.functions.basic_functions import end_process
from HousingPriceScraper.HousingPriceScraper.functions.data_management import read_txt_to_list
from HousingPriceScraper.HousingPriceScraper.functions.menus import basic_menu, select_spiders, set_config
from HousingPriceScraper.HousingPriceScraper.spiders.SpiderGroups.dummy_spiders import *
from HousingPriceScraper.HousingPriceScraper.spiders.SpiderGroups.property_spiders import *
from HousingPriceScraper.HousingPriceScraper.spiders.SpiderGroups.film_spiders import *


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


def find_visible_projects():
    """
    return list of set visible projects

    :return: list of visible projects
    """
    try:
        visible_projects = [i.replace('\n', '') for i in read_txt_to_list('HousingPriceScraper/HousingPriceScraper/configs/visible_projects_to_scrape.txt')]
    except FileNotFoundError:
        visible_projects = [i.split('.')[0] for i in os.listdir('HousingPriceScraper/HousingPriceScraper/spiders/SpiderGroups')[:-1]]
    return visible_projects


def create_spiders_list():
    """
    create list of spiders that obeys the visible projects list, through use of the spider selection menu

    :return: list of spiders
    """
    spiders_lst = [obj for obj in globals().values() if
                   inspect.isclass(obj) and str(obj).split('.')[2] == 'spiders' and 'BaseSpider' not in str(obj)]
    visible_projects = find_visible_projects()
    spiders_dict = {i.split('.')[0]: [obj for obj in spiders_lst if i.split('.')[0] in str(obj)] for i in
                    os.listdir('HousingPriceScraper/HousingPriceScraper/spiders/SpiderGroups')[:-1] if i.split('.')[0] in visible_projects}
    if len(list(spiders_dict.keys())) > 0:
        spiders_lst = select_spiders(spiders_dict)
    else:
        print('There are no visible projects, got to set_visible_projects to set defaults')
        return False
    return spiders_lst


def run_scrapers():
    """
    function to run scraping pipeline. will collate all read in spiders into a list and send it off to the reactor

    :return: will either run the scrapers, or will allow user to paginate back to main menu.
    """
    spiders_lst = create_spiders_list()
    if not spiders_lst:
        return True
    else:
        simultaneous_run(spiders_lst)


def scrape_menu():
    """
    function to interface with scrapers themselves.

    :return: takes you through the scraping menu with the #bois
    """
    options_dict = {'run_scrape': run_scrapers,
                    'set_run_config': set_config}
    basic_menu(options_dict, back=True)
    return True
