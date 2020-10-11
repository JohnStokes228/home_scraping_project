"""
the gooey interior of the spider, containing the scraping methods. html parsing is currently handled by beautiful soup.

TODO - investigate selenium: might be worth having another class for driver usage if its going to be needed?
     - element_to_attribute may need further updates as the find() method might be a bit ambiguous, we'll have to see
       how it behaves in practice
     - its likely that non identically structured websites may break a few of these methods we'll have to see as we
       get to them
"""
import time
from random import randint
from bs4 import BeautifulSoup


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

    def element_to_attribute(self, element_list, attribute):
        """
        function converts list of elements to equal length list of the desired attribute. Uses Beautiful Soup to parse
        the html.

        :param element_list: input list of str's, in form of html
        :param attribute: desired attribute to pull from each element
        :return: list of desired attributes
        """
        attribute_list = []
        for element in element_list:
            soup = BeautifulSoup(element, 'html.parser')
            if attribute == 'text':
                attribute_list.append(soup.get_text())
            else:
                attr = soup.find()[attribute]
                attribute_list.append(attr)
        return attribute_list

    def scrape_to_attribute(self, response, target_path, attribute, xpath=True):
        """
        function runs element_to_attribute(get_element())

        :param response: scrapy response object - the target url
        :param target_path: the xpath / css selector of the desired element
        :param attribute: the desired attribute i.e. href, a, etc...
        :param xpath: boolean indicating if target_path is xpath or css selector. defaults to xpath
        :return: list of attributes
        """
        element_list = self.get_element(response, target_path, xpath)
        attribute_list = self.element_to_attribute(element_list, attribute)
        return attribute_list

    def scrape_table_to_dict(self, response, var_col, var_attr, val_col, val_attr, xpath=True):
        """
        function to scrape a table of data into a dictionary

        :param response: scrapy response object
        :param var_col: column of table containing variable names
        :param var_attr: attribute for var_col path
        :param val_col: column of table containing variable realisations
        :param val_attr: value attribute
        :param xpath: boolean indicating if var_col and att_col are given by xpath or css selector
        :return: dictionary with keys = var_col and values = att_col
        """
        var_names = self.scrape_to_attribute(response, var_col, var_attr, xpath)
        vals = self.scrape_to_attribute(response, val_col, val_attr, xpath)
        table_dict = {var_names[i]: [vals[i]] for i in range(len(var_names))}
        return table_dict

    def scrape_multiple_to_attribute(self, response, list_of_tuples):
        """
        function that will scrape a list of tuples using the scrape_to_attribute function

        :param response: scrapy response object - the url of the site
        :param list_of_tuples: tuples of form (var_name, target_path, attribute, xpath=True (optional))
        :return: dictionary of chosen attributes, whose keys are the var_names from the tuples.
        """
        output_dict = {}
        for input_tuple in list_of_tuples:
            output_dict[input_tuple[0]] = self.scrape_to_attribute(response, *input_tuple[1:])
        return output_dict

    def scrape_product_box(self, response, product_path, attribute_lists_list, xpath=True):
        """
        scrape whole product cell from shelf level webpage. using this method should avoid any data alignment issues, by
        instead using Beautiful Soup to pull the attributes from specific products after first scraping all html related
        to said product.

        :param response: scrapy response object - the url of the site
        :param product_path: xpath or css selector pointing to the product cell
        :param attribute_lists_list: list of lists of form (var_name, node, node_index, attribute, condition (optional))
               condition must be a dictionary of form {attribute: attribute_value}
        :param xpath: boolean indicating if product_path is using xpath or css
        :return: dictionary of chosen attributes, whose keys are the var_names from attribute_tuples_list
        """
        output_dict = {var_name: [] for var_name in [tup[0] for tup in attribute_lists_list]}
        product_cell_list = self.get_element(response, product_path, xpath)

        for product_data in product_cell_list:
            soup = BeautifulSoup(product_data, 'html.parser')
            for attr_list in attribute_lists_list:
                if len(attr_list) < 5:
                    attr_list.append(None)
                if attr_list[3] == 'text':
                    output_dict[attr_list[0]].append(soup.find_all(attr_list[1], attrs=attr_list[4])[attr_list[2]].get_text())
                else:
                    output_dict[attr_list[0]].append(soup.find_all(attr_list[1], attrs=attr_list[4])[attr_list[2]][attr_list[3]])
        return output_dict
