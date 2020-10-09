"""
contains generic code for use in main menus. currently this is a function which turns dictionaries of functions
into a menu. I envision any further menu functions being stored here so don't expect it to run like a pipeline but
rather like a suite of individual menus.

TODO - it may be that some of these functions end up elsewhere as I can see end_process being useful...
     - I'm thinking an additional python file for generic functions such as the ones found at the top
       of this file
     - !!refactor select spiders into more legible code!!
"""
import string
import itertools
import re


def end_process():
    """
    function to correctly end the python process

    :return: exit with code 0
    """
    print('\ngoodbye!')
    exit(0)


def return_false():
    """
    function that returns False

    :return: True lol jk it returns False
    """
    return False


def alphabet_list():
    """
    create list of alphabetical letters with infinite length

    :return: alphabet list of given length
    """
    for size in itertools.count(1):
        for s in itertools.product(string.ascii_lowercase, repeat=size):
            yield "".join(s)


def alphabet_list_length(length, index=None):
    """
    run alphabet_list for a set length of output

    :param length: length of desired list
    :param index: string to match
    :return: alphabet list of given length
    """
    if index:
        alpha_list = []
        for alpha_ind in alphabet_list():
            alpha_list.append(alpha_ind)
            if alpha_ind == index:
                return alpha_list
    else:
        alpha_list = [alpha_ind for alpha_ind in itertools.islice(alphabet_list(), length)]
        return alpha_list


def flatten_list_of_lists(list_of_lists, make_set=False):
    """
    function to flatten list of lists into a single lists

    :param list_of_lists: list of lists
    :param make_set: boolean indicating if the output should deduplicate its elements
    :return: list
    """
    flat_list = [item for sublist in list_of_lists for item in sublist]
    if make_set:
        flat_list = list(set(flat_list))
    return flat_list


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
    print('{} - back\n'.format(len(spiders_dict.keys())+1))
    choices = input('\nfor multiple, comma separate. to remove, use "-" prefix\n')
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
            elif '-' not in choice:
                numeric = re.findall(r'\d+', choice)
                if len(numeric) == 1:
                    alpha = choice.split(numeric[0])[1]
                    alpha = len(alphabet_list_length(0, index=alpha))-1
                    try:
                        chosen_spiders.append(spiders_dict[enumerated_keys[int(numeric[0])][1]][alpha])
                    except IndexError:
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
                numeric = re.findall(r'\d+', removee)
                if len(numeric) == 1:
                    alpha = removee.split(numeric[0])[1]
                    alpha = len(alphabet_list_length(0, index=alpha)) - 1
                    try:
                        chosen_spiders.remove(spiders_dict[enumerated_keys[int(numeric[0])][1]][alpha])
                    except IndexError:
                        print('{} is not an option'.format(removee))
    if len(chosen_spiders) > 0:
        return chosen_spiders
    else:
        print("You haven't selected any spiders!")
        return False
