"""
function suite to coalate jsons into meaningful data.

TODO - write cleaning methods
     - write method to join attribute to regular data
"""
import os
from HousingPriceScraper.HousingPriceScraper.functions.menus import basic_menu, select_date_interval_menu, basic_menu_non_functional
from HousingPriceScraper.HousingPriceScraper.functions.basic_functions import print_pizza_time, date_today
from HousingPriceScraper.HousingPriceScraper.processes.run_scrapers import find_visible_projects
from HousingPriceScraper.HousingPriceScraper.functions.data_management import jsons_to_csv
from HousingPriceScraper.HousingPriceScraper.spiders.SpiderGroups.dummy_spiders import *


def coalate_data():
    """
    gives users options to coalate data from json into csv format

    :return: csv files for each chosen spider are sent to the transformed data folder
    """
    visible_projects = find_visible_projects()
    datas = []
    for project in visible_projects:
        project_data = os.listdir('HousingPriceScraper/HousingPriceScraper/data/raw_data/{}'.format(project))
        datas += ['{}/{}'.format(project, i) for i in project_data]
    chosen_datas = basic_menu_non_functional([i.split('/')[1] for i in datas])
    datas = [i for i in datas if i.split('/')[1] in chosen_datas]
    dates = select_date_interval_menu()
    for data in datas:
        jsons = []
        available_dates = [i for i in os.listdir('HousingPriceScraper/HousingPriceScraper/data/raw_data/{}'.format(data)) if i in dates]
        for date in available_dates:
            jsons += ['HousingPriceScraper/HousingPriceScraper/data/raw_data/{}/{}/{}'.format(data, date, i) for i in os.listdir('HousingPriceScraper/HousingPriceScraper/data/raw_data/{}/{}'.format(data, date))]
        items = [json_file for json_file in jsons if '_attrs_' not in json_file and 'FAIL' not in json_file]
        attrs = [json_file for json_file in jsons if '_attrs_' in json_file and 'FAIL' not in json_file]
        if len(items) > 0:
            jsons_to_csv(items, '{}-{}_{}'.format(dates[0], dates[-1], data.split('/')[1]))
        if len(attrs) > 0:
            jsons_to_csv(attrs, '{}-{}_{}_attrs'.format(dates[0], dates[-1], data.split('/')[1]))
    print('\n')
    return True


def coalate_all_data():
    """
    gives users options to coalate data from json into csv format

    :return: csv files for each chosen spider are sent to the transformed data folder
    """
    visible_projects = find_visible_projects()
    datas = []
    for project in visible_projects:
        project_data = os.listdir('HousingPriceScraper/HousingPriceScraper/data/raw_data/{}'.format(project))
        datas += ['{}/{}'.format(project, i) for i in project_data]
    chosen_datas = basic_menu_non_functional([i.split('/')[1] for i in datas])
    datas = [i for i in datas if i.split('/')[1] in chosen_datas]
    for data in datas:
        jsons = []
        available_dates = [i for i in os.listdir('HousingPriceScraper/HousingPriceScraper/data/raw_data/{}'.format(data))]
        for date in available_dates:
            jsons += ['HousingPriceScraper/HousingPriceScraper/data/raw_data/{}/{}/{}'.format(data, date, i) for i in os.listdir('HousingPriceScraper/HousingPriceScraper/data/raw_data/{}/{}'.format(data, date))]
        items = [json_file for json_file in jsons if '_attrs_' not in json_file and 'FAIL' not in json_file]
        attrs = [json_file for json_file in jsons if '_attrs_' in json_file and 'FAIL' not in json_file]
        if len(items) > 0:
            jsons_to_csv(items, 'start-{}_{}'.format(date_today(), data.split('/')[1]))
        if len(attrs) > 0:
            jsons_to_csv(attrs, 'start-{}_{}_attrs'.format(date_today(), data.split('/')[1]))
    print('\n')
    return True


def data_management_menu():
    """
    menu options for the data management function suite.

    :return: takes you through the data management menu
    """
    options_dict = {'coalate_data_custom_interval': coalate_data,
                    'coalate_all_data': coalate_all_data,
                    'clean_data': print_pizza_time,
                    'join_attributes': print_pizza_time}
    basic_menu(options_dict, back=True)
    return True
