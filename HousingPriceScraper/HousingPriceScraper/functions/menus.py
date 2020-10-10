"""
contains generic code for use in main menus. currently this is a function which turns dictionaries of functions
into a menu. I envision any further menu functions being stored here so don't expect it to run like a pipeline but
rather like a suite of individual menus.

TODO - **refactor select spiders into more legible code**
     - write menu to update the visible spider projects.
"""
import re
import os
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
    choices = input('\nfor multiple, comma separate. To remove, use "-" prefix\ni.e.: 0,-0a to run all of group 0 except the first\n')
    choices = choices.split(',')
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
    chosen_spiders = flatten_list_of_lists(chosen_spiders, make_set=True)
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
    projects = [i.split('.')[0] for i in os.listdir('spiders/SpiderGroups')[:-1]]
    print('Available projects are:\n')
    for project in enumerate(projects):
        print('\t{} - {}'.format(project[0], project[1]))
    print('\t{} - back'.format(len(projects)+1))
    choices = input('\nType the options you wish to select.\nFor multiple, comma separate\n\n').split(',')
    if str(len(projects)+1) in choices:
        return True
    else:
        choice_list = []
        for choice in choices:
            if choice.isdigit() and int(choice) in range(len(projects)):
                choice_list.append(projects[int(choice)])
        print('You have selected to display the following spider groupings:\n\t{}\n'.format(choice_list))
        save_list_to_txt(choice_list, 'configs/visible_projects_to_scrape.txt')
        return True
