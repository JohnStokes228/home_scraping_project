"""
includes Selenium features, to allow the spider to 'see' the website and, y'know, poke about on it I guess

TODO - write basic interactivity methods
     - write replacements for all the existing scrapy / beautifulsoup4 methods
     - I would like to investigate whether it might be possible to make this not inherit AncestorSpider
       but rather be just another piece of the puzzle prehaps?
"""
from selenium import webdriver
from random import randint
import time
import os
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider


class PerceptiveAncestorSpider(AncestorSpider):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome(executable_path="{}/spiders/AncestorSpider/chromedriver.exe".format(os.getcwd()))

    def get_url(self, response):
        """
        function for visiting url using chromedriver

        :return: opens url and waits a random number of seconds
        """

        self.driver.get(response.url)
        time.sleep(randint(2, 6))

    def close(spider, reason):
        """
        method for end of scrape

        :param reason: reason for closure of spider - unused just comes in as default.
        :return: proper finish
        """

        spider.driver.quit()

