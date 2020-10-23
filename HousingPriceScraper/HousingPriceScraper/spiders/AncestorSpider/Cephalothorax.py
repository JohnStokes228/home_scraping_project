"""
includes Selenium features, to allow the spider to 'see' the website and, y'know, poke about on it I guess

TODO - write basic interactivity methods
     - * write scrape cell to attribute method replacement *
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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

    def driver_get_element(self, target_path, xpath=True, multiple=True):
        """
        selenium integrated version of abdomens 'get_element' method

        :param target_path: xpath of target element
        :param multiple: boolean indicating if expect multiple elements or if only one
        :param xpath: boolean set False to use CSS
        :return: list element
        """
        time.sleep(randint(2, 6))
        if not multiple:
            if xpath:
                element = self.driver.find_element(By.XPATH, target_path)
            else:
                element = self.driver.find_element(By.CSS_SELECTOR, target_path)
        else:
            if xpath:
                element = self.driver.find_elements(By.XPATH, target_path)
            else:
                element = self.driver.find_elements(By.CSS_SELECTOR, target_path)
        return element

    def driver_elements_to_attribute(self, element_list, attribute):
        """
        selenium integrated version of function converts list of elements to equal length list of the
        desired attribute.

        :param element_list: input list of str's, in form of html
        :param attribute: desired attribute to pull from each element
        :return: list of desired attributes
        """
        if isinstance(element_list, list):
            attribute_list = []
            for element in element_list:
                if attribute == 'text':
                    attribute_list.append(element.text)
                else:
                    attribute_list.append(element.get_attribute(attribute))
            return attribute_list
        else:
            if attribute == 'text':
                attribute = element_list.text
            else:
                attribute = element_list.get_attribute(attribute)
            return attribute

    def driver_scrape_to_attribute(self, target_path, attribute, xpath=True, multiple=True):
        """
        selenium integrated function runs driver_element_to_attribute(driver_get_element())

        :param target_path: the xpath / css selector of the desired element
        :param attribute: the desired attribute i.e. href, a, etc...
        :param multiple: boolean indicating if the scrape is singular or multiple
        :param xpath: boolean indicating if target_path is xpath or css selector. defaults to xpath
        :return: list of attributes
        """

        elements = self.driver_get_element(target_path, multiple, xpath)
        attributes = self.driver_elements_to_attribute(elements, attribute)
        return attributes

    def driver_scrape_table_to_dict(self, var_col, var_attr, val_col, val_attr, xpath=True):
        """
        selenium integrated function to scrape a table of data into a dictionary

        :param var_col: column of table containing variable names
        :param var_attr: attribute for var_col path
        :param val_col: column of table containing variable realisations
        :param val_attr: value attribute
        :param xpath: boolean indicating if var_col and att_col are given by xpath or css selector
        :return: dictionary with keys = var_col and values = att_col
        """

        var_names = self.driver_scrape_to_attribute(var_col, var_attr, xpath)
        vals = self.driver_scrape_to_attribute(val_col, val_attr, xpath)
        table_dict = {var_names[i]: [vals[i]] for i in range(len(var_names))}
        return table_dict

    def driver_scrape_multiple_to_attribute(self, list_of_tuples):
        """
        selenium integrated function that will scrape a list of tuples using the scrape_to_attribute function

        :param list_of_tuples: tuples of form (var_name, target_path, attribute, xpath=True (optional))
        :return: dictionary of chosen attributes, whose keys are the var_names from the tuples.
        """

        output_dict = {}
        for input_tuple in list_of_tuples:
            output_dict[input_tuple[0]] = self.driver_scrape_to_attribute(*input_tuple[1:])
        return output_dict

    def driver_scrape_product_box(self, product_path, attribute_lists_list, xpath=True, multiple=True):
        """
        selenium integrated scrape whole product cell from shelf level webpage. using this method should
        avoid any data alignment issues, by instead using Beautiful Soup to pull the attributes from specific
        products after first scraping all html related to said product. code might need to be tweaked as its currently
        the exact code i used to write this method for ONS...

        :param product_path: xpath or css selector pointing to the product cell
        :param attribute_lists_list: list of lists of form (var_name, xpath, attribute), where xpath starts with a
               single / and can be indexed using [] starting from 1.
        :param xpath: boolean indicating if product_path is using xpath or css
        :param multiple: boolean indicating if there are multiple elements cells to scrape
        :return: dictionary of chosen attributes, whose keys are the var_names from attribute_tuples_list
        """

        output_dict = {var_name: [] for var_name in [tup[0] for tup in attribute_lists_list]}
        product_cell_list = self.driver_get_element(product_path, xpath, multiple)
        for target_element in attribute_lists_list:
            for cell in product_cell_list:
                attrs = cell.find_elements_by_xpath('.{}'.format(target_element[1]))
                attrs = self.driver_elements_to_attribute(attrs, target_element[2])
                if 0 < len(attrs) < 1:
                    output_dict[target_element[0]].append(attrs)
                elif len(attrs) == 0:
                    output_dict[target_element[0]].append('')
                else:
                    output_dict[target_element[0]].append(attrs[0])
        return output_dict

    def find_press_button(self, xpath):
        """
        find a button via xpath and then click it.

        :param xpath: xpath for the button. I see no need for css to be an option ever here
        :return: the button is clicked you hear me!! but legit though nothing is returned here calm down pls
        """
        try:
            button = self.driver_get_element(xpath, multiple=False)
            time.sleep(randint(1, 3))
            try:
                button.click()
                return True
            except:
                print('button not clickable!')
                return False
        except NoSuchElementException:
            print('button not found!')
            return False

    def scroll_to_bottom(self, number_of_stops=3):
        """
        selenium driver function that will scroll down to the bottom of a webpage, in number_of_stops unique intervals.
        this function is built to deal with infinite scrolls, as well as pages that require sight on cells to load the
        content.

        :param number_of_stops: an integer dictating the number of stops along the way you hit whilst scrolling.
        :return: WebDriver will scroll down a page until it finds an element
        """
        current_bottom = self.driver.execute_script("return document.body.scrollHeight")
        keep_scrolling = True
        while keep_scrolling:
            for i in range(0, number_of_stops):
                self.driver.execute_script("window.scrollTo({}, {});".format((i*(current_bottom/number_of_stops)), ((i+1)*(current_bottom/number_of_stops))))
                time.sleep(randint(1, 3))
            new_bottom = self.driver.execute_script("return document.body.scrollHeight")
            if new_bottom == current_bottom:
                keep_scrolling = False
            else:
                current_bottom = new_bottom

    def close(spider, reason):
        """
        method for end of scrape

        :param reason: reason for closure of spider - unused just comes in as default.
        :return: proper finish
        """

        spider.driver.quit()
