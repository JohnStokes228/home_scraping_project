"""
the gooey interior of the spider, containing the scraping methods

TODO - write a function that saves data
     - investigate selenium
"""
import time
from random import randint


class SpiderMethods:

    def get_element(self, response, target_path, xpath=True):
        """
        function to get element from response

        :param response: response obj from scrapy
        :param target_path: an xpath or css selector pointing to the desired element
        :param xpath: true for xpath, false for css. determines how to handle target_path
        :return: element
        """
        time.sleep(randint(0, 3))
        if xpath:
            element = response.xpath(target_path).extract()
        else:
            element = response.css(target_path).extract()
        return element
