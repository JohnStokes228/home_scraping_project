"""
function suite to coalate jsons into meaningful data.

TODO - write cleaning methods - does it not make sense to build a separate cleaning pipeline somewhere?
     - yeah i think cleaning and classifying should be its own follow on project
     - rewrite method for joining attribute to item data such that it is more robust.
"""
import os
import pandas as pd
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


def join_attributes_to_items():
    """
    function to join attribute file to item file and output as a single 'complete' csv

    :return: single combined csv
    """
    data_base_dir = 'HousingPriceScraper/HousingPriceScraper/data/transformed_data'
    files = [file for file in os.listdir(data_base_dir)]
    spiders = list(set([file.split('_')[1].replace('.csv', '') for file in files]))
    for spider in spiders:
        attr_files = [file for file in files if 'attrs' in file and spider in file]
        items_files = [file for file in files if 'attrs' not in file and spider in file]
        if len(items_files) > 0:
            items_files = [pd.read_csv('{}/{}'.format(data_base_dir, item)) for item in items_files]
            df = pd.concat(items_files)
            if len(attr_files) > 0:
                attr_files = [pd.read_csv('{}/{}'.format(data_base_dir, attr)) for attr in attr_files]
                attr_df = pd.concat(attr_files)
                attr_df.drop_duplicates(subset=attr_df.columns.difference(['time_scraped', 'date_scraped']))
                join_cols = [col for col in df.columns if col in attr_df.columns and col not in ['time_scraped', 'date_scraped']]
                df = df.merge(attr_df, on=join_cols, how='left')
            df.to_csv('{}/complete_transformed_data/{}_complete.csv'.format(data_base_dir, spider), index=False)
            print('successfully saved complete data for spider {} to file:\n\t{}_complete.csv'.format(spider, spider))
        else:
            print('impossible to complete files for spider {}'.format(spider))
    return True


def data_management_menu():
    """
    menu options for the data management function suite.

    :return: takes you through the data management menu
    """
    options_dict = {'coalate_data_custom_interval': coalate_data,
                    'coalate_all_data': coalate_all_data,
                    'join_attributes': join_attributes_to_items,
                    'clean_data': print_pizza_time}
    basic_menu(options_dict, back=True)
    return True
