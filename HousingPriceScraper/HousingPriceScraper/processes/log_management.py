"""
the next (final?) menu option to be added to the project, will include options for tracking content of logs
over time.

"""
from HousingPriceScraper.HousingPriceScraper.functions.menus import basic_menu
from HousingPriceScraper.HousingPriceScraper.functions.basic_functions import print_pizza_time


def log_management_menu():
    """
    entry way into the wonderous world of my garbage low level logging.

    :return: it'll give you a menu to click through like the bitch you are
    """
    options_dict = {'view_most_recent_logs': print_pizza_time,
                    'clear_logs': print_pizza_time,
                    'highlight_issues': print_pizza_time}
    basic_menu(options_dict, back=True)
    return True
