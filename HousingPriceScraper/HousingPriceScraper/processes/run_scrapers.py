"""
file containing code to run spiders, called from main.py if run_scrape is selected.

TODO - write method to get list of spiders: basically done, though there'll need to be some further work here to filter
       it all down once we know the extent of what isn't a spider in this project
     - incorporate the menus to allow user to manually reduce the list of spiders.
     - add menu to allow user to specify configuration of input urls
     - allow shelf, item and combination spiders to be run using some for of intuitive menu
     - write multiprocessing implementation - crochet/pathos worked before but is there a more elegant solution?
     - import spider settings for use in crawler process.
"""
import inspect
from scrapy.crawler import CrawlerProcess
from HousingPriceScraper.HousingPriceScraper.functions.menus import end_process
from HousingPriceScraper.HousingPriceScraper.spiders.DummySpiders.DummyBooks import DummyBooksSpider
from HousingPriceScraper.HousingPriceScraper.spiders.DummySpiders.DummyQuotes import DummyQuotesSpider


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
    spiders_lst = [obj for obj in globals().values() if inspect.isclass(obj) and str(obj).split('.')[2] == 'spiders']
    simultaneous_run(spiders_lst)
    return True
