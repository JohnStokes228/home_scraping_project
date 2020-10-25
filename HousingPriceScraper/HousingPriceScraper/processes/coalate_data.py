"""
function suite to coalate jsons into meaningful data.

TODO - coalate data needs to be smart as to how it finds data to coalate
     - need to rewrite the selection method so its not borked - don't think it needs to utilise the current spider
       selector at all no sir.
     - make changes to the way data is saved based on how this goes.
"""
from HousingPriceScraper.HousingPriceScraper.functions.menus import basic_menu, select_date_interval_menu
from HousingPriceScraper.HousingPriceScraper.functions.basic_functions import print_pizza_time
from HousingPriceScraper.HousingPriceScraper.processes.run_scrapers import create_spiders_list
from HousingPriceScraper.HousingPriceScraper.spiders.SpiderGroups.dummy_spiders import *


def coalate_data():
    """
    gives users options to coalate data from json into csv format

    :return: csv files for each chosen spider are sent to the transformed data folder
    """
    spiders_lst = create_spiders_list()
    if not spiders_lst:
        print('No spiders Selected')
        return True
    else:
        spiders_lst = [i.name for i in spiders_lst if 'combi' not in i.name]
        dates = select_date_interval_menu()
        # we'll now have to go searching for some data bro. its gonna be mad. trust.
        return True


def data_management_menu():
    """
    menu options for the data management function suite.

    :return: takes you through the data management menu
    """
    options_dict = {'coalate_data': coalate_data,
                    'clean_data': print_pizza_time,
                    'join_attributes': print_pizza_time}
    basic_menu(options_dict, back=True)
    return True
