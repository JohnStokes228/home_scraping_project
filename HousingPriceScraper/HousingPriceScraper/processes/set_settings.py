"""
covers all the settings the user can tweak for the project

"""
import json
import os
from datetime import datetime
from HousingPriceScraper.HousingPriceScraper.functions.menus import append_recent_urls, replace_default_urls, create_new_config, clear_recent_urls, basic_menu, project_visibility_menu


def get_recent_missed():
    """
    gets the most recent values of missed urls from the log files

    :return: a dictionary whose keys are spider names and values are lists of missed urls
    """
    missed_urls = {}
    for log_file in os.listdir('HousingPriceScraper/HousingPriceScraper/data/scrape_logs'):
        with open('HousingPriceScraper/HousingPriceScraper/data/scrape_logs/{}'.format(log_file)) as log_json:
            log_dict = json.load(log_json)
        max_date = max([datetime.strptime(i, '%d%m%Y') for i in log_dict.keys()]).strftime('%d%m%Y')
        if log_dict['missed_urls'] != ['']:
            missed_urls[log_file.replace('.json', '')] = log_dict[max_date]['missed_urls']
    return missed_urls


def remove_missed_from_default():
    """
    removes any missed urls from the default urls config, if they are in it.

    :return: saves new defaults config, this time without any missed urls in
    """
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/defaults.json') as defaults_json:
        defaults_dict = json.load(defaults_json)
    missed_urls = get_recent_missed()
    for spider in defaults_dict.keys():
        if spider in missed_urls.keys():
            defaults_dict[spider] = [i for i in defaults_dict[spider] if i not in missed_urls[spider]]
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/defaults.json', 'w') as fp:
        json.dump(defaults_dict, fp, sort_keys=True, indent=4)
    print('recently missed urls removed from default config\n')


def create_missed_config():
    """
    function which creates a whole new config file to store recently missed urls in

    :return: new config is created
    """
    missed_urls = get_recent_missed()
    config_name = 'missed_urls'
    config_desc = 'urls missed from most recent scrapes'
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/{}.json'.format(config_name), 'w') as fp:
        json.dump(missed_urls, fp, sort_keys=True, indent=4)
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_url_config_descriptions.txt', 'a') as input_descs:
        input_descs.write('\n{}: {}'.format(config_name, config_desc))
    print('\nSuccessfully saved missed urls to new config: missed_urls.json')


def missed_config_manager():
    """
    function to deal with the missed urls in the logs

    :return: list of options
    """
    options = {'create_missed_config': create_missed_config,
               'remove_missed_from_default': remove_missed_from_default
               }
    basic_menu(options, back=True)
    return True


def recent_config_manager():
    """
    function to refresh item urls for all? or maybe just specified spiders in a variety of ways

    :return:
    """

    options = {'append_recent_to_default': append_recent_urls,
               'overwrite_default': replace_default_urls,
               'create_new_config': create_new_config,
               'clear_recent_urls': clear_recent_urls
               }
    basic_menu(options, back=True)
    return True


def settings_menu():
    """
    main menu for settings

    :return: select settings or go back
    """
    options = {'set_visible_projects': project_visibility_menu,
               'recent_urls_options': recent_config_manager,
               'missed_urls_options': missed_config_manager
               }
    basic_menu(options, back=True)
    return True
