"""
includes Selenium features, to allow the spider to 'see' the website and, y'know, poke about on it I guess

TODO - write basic interactivity methods
     - * write replacements for all the existing scrapy / beautifulsoup4 methods. there are defs written for
       each already *
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
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

    def driver_get_element(self, target_xpath, multiple=True, xpath=True):
        """
        selenium integrated version of abdomens 'get_element' method

        :param target_xpath: xpath of target element
        :param multiple: boolean indicating if expect multiple elements or if only one
        :param xpath: boolean set False to use CSS
        :return: element
        """
        time.sleep(randint(2, 6))
        if not multiple:
            if xpath:
                element = self.driver.find_element(By.XPATH, target_xpath)
            else:
                element = self.driver.find_element(By.CSS_SELECTOR, target_xpath)
        else:
            if xpath:
                element = self.driver.find_elements(By.XPATH, target_xpath)
            else:
                element = self.driver.find_elements(By.CSS_SELECTOR, target_xpath)
        return element

    def driver_element_to_attribute(self, element_list, attribute):
        """
        selenium integrated version of function converts list of elements to equal length list of the
        desired attribute.

        :param element_list: input list of str's, in form of html
        :param attribute: desired attribute to pull from each element
        :return: list of desired attributes
        """

        pass

    def driver_scrape_to_attribute(self, target_path, attribute, multiple=True, xpath=True):
        """
        selenium integrated function runs driver_element_to_attribute(driver_get_element())

        :param response: scrapy response object - the target url
        :param target_path: the xpath / css selector of the desired element
        :param attribute: the desired attribute i.e. href, a, etc...
        :param xpath: boolean indicating if target_path is xpath or css selector. defaults to xpath
        :return: list of attributes
        """

        pass

    def driver_scrape_table_to_dict(self, response, var_col, var_attr, val_col, val_attr, xpath=True):
        """
        selenium integrated function to scrape a table of data into a dictionary

        :param response: scrapy response object
        :param var_col: column of table containing variable names
        :param var_attr: attribute for var_col path
        :param val_col: column of table containing variable realisations
        :param val_attr: value attribute
        :param xpath: boolean indicating if var_col and att_col are given by xpath or css selector
        :return: dictionary with keys = var_col and values = att_col
        """

        pass

    def driver_scrape_multiple_to_attribute(self, response, list_of_tuples):
        """
        selenium integrated function that will scrape a list of tuples using the scrape_to_attribute function

        :param response: scrapy response object - the url of the site
        :param list_of_tuples: tuples of form (var_name, target_path, attribute, xpath=True (optional))
        :return: dictionary of chosen attributes, whose keys are the var_names from the tuples.
        """

        pass

    def driver_scrape_product_box(self, response, product_path, attribute_lists_list, xpath=True):
        """
        selenium integrated scrape whole product cell from shelf level webpage. using this method should
        avoid any data alignment issues, by instead using Beautiful Soup to pull the attributes from specific
        products after first scraping all html related to said product.

        :param response: scrapy response object - the url of the site
        :param product_path: xpath or css selector pointing to the product cell
        :param attribute_lists_list: list of lists of form (var_name, node, node_index, attribute, condition (optional))
               condition must be a dictionary of form {attribute: attribute_value}
        :param xpath: boolean indicating if product_path is using xpath or css
        :return: dictionary of chosen attributes, whose keys are the var_names from attribute_tuples_list
        """

        pass

    def close(spider, reason):
        """
        method for end of scrape

        :param reason: reason for closure of spider - unused just comes in as default.
        :return: proper finish
        """

        spider.driver.quit()
