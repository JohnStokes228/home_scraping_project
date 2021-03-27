"""
contains generic code for use in main menus. currently this is a function which turns dictionaries of functions
into a menu. I envision any further menu functions being stored here so don't expect it to run like a pipeline but
rather like a suite of individual menus.

TODO - refactor spider selection function as jesus christ that things fat
     - incorporate spider selector in config manager options
"""
import re
import os
import json
from datetime import date, datetime
from collections import defaultdict
import pandas as pd
from HousingPriceScraper.HousingPriceScraper.functions.basic_functions import return_false, end_process, \
    alphabet_list_length, flatten_list_of_lists
from HousingPriceScraper.HousingPriceScraper.functions.data_management import save_list_to_txt


def final_option(dict_of_options, back):
    """
    adds the final option to the dictionary based on a boolean

    :param dict_of_options: dictionary with readable labels as keys and uncalled functions as values. It is important
           that these functions don't require parameters.
    :param back: boolean
    :return: dict_of_options but with a new, final key added in
    """
    if back:
        dict_of_options['back'] = return_false
    else:
        dict_of_options['end_process'] = end_process
    return dict_of_options


def basic_menu(dict_of_options, back=False):
    """
    basic text based user interface, allows user to select a function to run from a dictionary of options, by using a
    simple numeric code. User will see this dictionaries keys enumerated on screen to choose from.

    :param dict_of_options: dictionary with readable labels as keys and uncalled functions as values. It is important
           that these functions don't require parameters.
    :param back: boolean. choose between scrolling back to previous menu or ending the process entirely. defaults to
           ending process since that's how the main menu does it and unsure of where else function will be called
    :return: run the chosen function
    """
    choose = True
    dict_of_options = final_option(dict_of_options, back)
    list_of_options = list(dict_of_options.keys())

    while choose:
        print('The following options are available:\n')
        for option in enumerate(list_of_options):
            print('\t{} - {}'.format(option[0], option[1]))
        pick = input('\nType the numeric code you wish to run\n\n')
        if pick in [str(i) for i in range((len(dict_of_options)))]:
            choose = dict_of_options[list_of_options[int(pick)]]()
        else:
            print('{} is not currently an option!\n'.format(pick))


def basic_menu_non_functional(list_of_options):
    """
    basic text based user interface, allows user to select multiple options from a list of available choices.

    :param list_of_options: list of available choices
    :return: a list of chosen strings
    """
    choose = True
    list_of_options.append('back')

    while choose:
        print('The following options are available:\n')
        for option in enumerate(list_of_options):
            print('\t{} - {}'.format(option[0], option[1]))
        picks = input('\nType the numeric codes you wish to run\n\n').split(',')
        choice = []
        if str(len(list_of_options)) in picks:
            return True
        for pick in picks:
            if pick in [str(i) for i in range((len(list_of_options)))]:
                choice.append(list_of_options[int(pick)])
            else:
                print('{} is not currently an option!\n'.format(pick))
        if len(choice) > 0:
            return choice


def select_spiders(spiders_dict):
    """
    select from spiders available. allows user to select all spiders, select all spiders within a
    project group, select some comma separated list of individual/groups of spiders, or by prefixing a
    given selection with "-", the user can remove a spider from his or her selection.

    :param spiders_dict: dictionary who's keys are broad options and values are lists of spiders
    :return: list containing the spiders the user has selected to run
    """
    print('Available spiders include:\n')
    enumerated_keys = list(enumerate(spiders_dict.keys()))
    for key_group in enumerated_keys:
        print('{} - {}'.format(key_group[0], key_group[1]))
        for spider in zip(alphabet_list_length(len(key_group[1])), spiders_dict[key_group[1]]):
            print('\t{}{} - {}'.format(key_group[0], spider[0], spider[1].name))
    print('{} - run all'.format(len(spiders_dict.keys())))
    print('{} - back'.format(len(spiders_dict.keys())+1))
    choices = input('\nfor multiple, comma separate. To remove, use "-" prefix\ni.e.: 0,-0a to run all of group 0 except the first\n').replace(' ', '').split(',')
    if str(len(spiders_dict.keys())+1) in choices:
        return False
    if str(len(spiders_dict.keys())) in choices:
        chosen_spiders = list(spiders_dict.values())
    else:
        chosen_spiders = []
        for choice in choices:
            if choice.isdigit():
                if choice in [str(i[0]) for i in enumerated_keys]:
                    chosen_spiders.append(spiders_dict[enumerated_keys[int(choice)][1]])
                else:
                    print('{} is not an option!'.format(choice))
            elif '-' not in choice:
                numeric = re.findall(r'\d+', choice)
                if len(numeric) == 1:
                    alpha = choice.split(numeric[0])[1]
                    alpha = len(alphabet_list_length(0, index=alpha))-1
                    try:
                        chosen_spiders.append(spiders_dict[enumerated_keys[int(numeric[0])][1]][alpha])
                    except IndexError:
                        print('{} is not an option!'.format(choice))
                else:
                    print('{} is not an option!'.format(choice))
    if any(isinstance(el, list) for el in chosen_spiders):
        chosen_spiders = flatten_list_of_lists(chosen_spiders, make_set=True)
    else:
        chosen_spiders = list(set(chosen_spiders))
    to_remove = [choice for choice in choices if '-' in choice]
    if len(to_remove) > 0:
        for removee in to_remove:
            if removee.replace('-', '').isdigit():
                if removee.replace('-', '') in [str(i[0]) for i in enumerated_keys]:
                    for spider in spiders_dict[enumerated_keys[int(removee.replace('-', ''))][1]]:
                        chosen_spiders.remove(spider)
                else:
                    print('{} is not an option!'.format(removee))
            else:
                numeric = re.findall(r'\d+', removee)
                if len(numeric) == 1:
                    alpha = removee.split(numeric[0])[1]
                    alpha = len(alphabet_list_length(0, index=alpha)) - 1
                    try:
                        chosen_spiders.remove(spiders_dict[enumerated_keys[int(numeric[0])][1]][alpha])
                    except IndexError:
                        print('{} is not an option!'.format(removee))
                else:
                    print('{} is not an option!'.format(removee))
    if len(chosen_spiders) > 0:
        return chosen_spiders
    else:
        print("You haven't selected any spiders!")
        return False


def project_visibility_menu():
    """
    creates menu to allow user to set which project groups are visible in the run_scrapers menu

    :return: creates a txt file containing the list of desired project names, one per row.
    """
    projects = [i.split('.')[0] for i in os.listdir('HousingPriceScraper/HousingPriceScraper/spiders/SpiderGroups')[:-1]]
    print('Available projects are:\n')
    for project in enumerate(projects):
        print('\t{} - {}'.format(project[0], project[1]))
    print('\t{} - back'.format(len(projects)))
    choices = input('\nType the options you wish to select.\nFor multiple, comma separate\n\n').split(',')
    if str(len(projects)) in choices:
        return True
    else:
        choice_list = []
        for choice in choices:
            if choice.isdigit() and int(choice) in range(len(projects)):
                choice_list.append(projects[int(choice)])
        print('You have selected to display the following spider groupings:\n\t{}\n'.format(choice_list))
        save_list_to_txt(choice_list, 'HousingPriceScraper/HousingPriceScraper/configs/visible_projects_to_scrape.txt')
        return True


def set_config():
    """
    menu to set the url configs.

    :return: will set the start_urls of the spiders.
    """
    available_configs = open('HousingPriceScraper/HousingPriceScraper/configs/input_url_config_descriptions.txt', 'r')
    options = available_configs.readlines()
    options_dict = {}
    print('available configs include:\n')
    for option in enumerate(options):
        options_dict[option[0]] = option[1].split(':')[0]
        print('\t{} - {}'.format(option[0], option[1].replace('\n', '')))
    print('\t{} - back'.format(len(options)))
    chosen = input('\ncomma separate for multiple\n').split(',')
    if (str(len(options)) in chosen) or (chosen == ['']):
        return True
    configs = []
    for choice in chosen:
        if int(choice) in options_dict:
            with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/{}.json'.format(options_dict[int(choice)])) as f:
                configs.append(json.load(f))
    final_config = defaultdict(list)
    for config in configs:
        for key, value in config.items():
            if key in final_config:
                final_config[key] += value
            else:
                final_config[key] = value
        for key, value in final_config.items():
            if any(isinstance(val, list) for val in value):
                final_config[key] = flatten_list_of_lists(value, make_set=True)
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/defaults.json') as default_urls_json:
        default_dict = json.load(default_urls_json)
    for key, value in default_dict.items():
        if key not in final_config.keys():
            final_config[key] = value
    with open('HousingPriceScraper/HousingPriceScraper/configs/chosen_urls.json', 'w') as fp:
        json.dump(final_config, fp, sort_keys=True, indent=4)
    return True


def append_recent_urls():
    """
    function for appending recent scraped urls to default urls json

    :return: default.json is updated
    """
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/defaults.json') as default_urls_json:
        default_dict = json.load(default_urls_json)
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/recent_urls.json') as recent_urls_json:
        recent_dict = json.load(recent_urls_json)
    for key, value in recent_dict.items():
        default_dict.setdefault(key, []).extend(value)
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/defaults.json', 'w') as fp:
        json.dump(default_dict, fp, sort_keys=True, indent=4)


def replace_default_urls():
    """
    function for replacing default urls config with recent scrapes

    :return: defaults.json is updated
    """
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/defaults.json') as default_urls_json:
        default_dict = json.load(default_urls_json)
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/recent_urls.json') as recent_urls_json:
        recent_dict = json.load(recent_urls_json)
    for key, value in recent_dict.items():
        default_dict[key] = value
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/defaults.json', 'w') as fp:
        json.dump(default_dict, fp, sort_keys=True, indent=4)


def create_new_config():
    """
    function which creates a whole new config file to store recent scraped urls in

    :return: new config is created
    """
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/recent_urls.json') as recent_urls_json:
        urls_dict = json.load(recent_urls_json)
    config_name = input('Type a name for the new config file:\n').replace(' ', '_').replace(':', '')
    config_desc = input('Type a brief description for the new config file:\n')
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/{}.json'.format(config_name), 'w') as fp:
        json.dump(urls_dict, fp, sort_keys=True, indent=4)
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_url_config_descriptions.txt', 'a') as input_descs:
        input_descs.write('\n{}: {}'.format(config_name, config_desc))
    print('\nSuccessfully saved recently scraped urls to new config: {}.json'.format(config_name))


def clear_recent_urls():
    """
    function which bleaches the recent urls config in order to start fresh next time

    :return: recent_urls will become an empty dictionary.
    """
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/recent_urls.json') as recent_urls_json:
        recent_dict = json.load(recent_urls_json)
    for key in recent_dict.keys():
        recent_dict[key] = []
    with open('HousingPriceScraper/HousingPriceScraper/configs/input_urls/recent_urls.json', 'w') as fp:
        json.dump(recent_dict, fp, sort_keys=True, indent=4)


def select_date_interval_menu():
    """
    function allows user to inout start and end date to define an interval of dates

    :return: list of dates
    """
    while True:
        start_date = input('\nInput desired start date with format dd-mm-yyyy:\n')
        try:
            start_date = datetime.strptime(start_date, '%d-%m-%Y')
            break
        except ValueError:
            print('invalid start date selected')
    while True:
        end_date = input('\nInput desired start date with format dd-mm-yyyy,\nor hit enter to select todays date\n')
        if end_date == '':
            end_date = date.today()
            break
        else:
            try:
                end_date = datetime.strptime(end_date, '%d-%m-%Y')
                break
            except ValueError:
                print('invalid end date selected')
    list_of_dates = pd.date_range(start_date, end_date, freq='d')
    list_of_dates = [i.strftime('%d%m%Y') for i in list_of_dates]
    return list_of_dates
