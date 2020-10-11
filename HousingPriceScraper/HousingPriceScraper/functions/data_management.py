"""
functions used to store or interact with the data. currently includes date related functions too.

TODO - will eventually need to write a suite of functions to interact with data and its structures
     - I wonder if these should be another class for the spiders to inherit? i.e. scraped_data_handler
       so it'd all be self. methods rather than function calls...?
     - its possible the column blower upperer might want to run after the read in rather than before.
"""
from pathlib import Path
import json
import itertools
import time
from HousingPriceScraper.HousingPriceScraper.functions.basic_functions import date_today, current_time


def check_make_dir(folder):
    """
    checks if folder exists, and if not, creates it

    :param folder: folder to check for / makes name. accepts multiple layers
    :return: sticks the folder where the sun don't shine
    """
    Path('{}'.format(folder)).mkdir(parents=True, exist_ok=True)
    print('directory ready at {}'.format(folder))


def save_dict_to_json(data_dict, file_path, file_name, date_vars=True, attrs=False):
    """
    you'll never guess what this function does :O

    :param data_dict: standard python dictionary object
    :param file_path: path to the output file
    :param file_name: the name given to the output file, will typically be spider name in this project
    :param date_vars: binary indicating whether to add variables for date and time of scrape
    :param attrs: boolean dictating if data is at attribute or shelf level
    :return: saves the input dictionary to a json file named with structure
    """
    time.sleep(1)
    if date_vars:
        data_dict['date_scraped'] = [date_today()] * len(data_dict[list(data_dict.keys())[0]])
        data_dict['time_scraped'] = [current_time()] * len(data_dict[list(data_dict.keys())[0]])
    if not attrs:
        file_name = '{}_{}_{}.json'.format(date_today(), current_time(), file_name)
    else:
        file_name = '{}_{}_attrs_{}.json'.format(date_today(), current_time(), file_name)
    with open('{}/{}'.format(file_path, file_name), 'w') as fp:
        json.dump(data_dict, fp, sort_keys=True, indent=4)
    print('data saved to file:\n\t{}'.format(file_name))


def expand_list_variable(data_dict, list_variable, delete_old_var=True):
    """
    function will expand a list of lists into separate lists of length 1 each within the data_dict

    :param data_dict: dictionary of data, including one key equal to list_variable
    :param list_variable: the variable name of the list variable
    :param delete_old_var: if True, will delete list_variable after use
    :return: data_dict but with the final key blown up into many, and the original variable deleted
    """
    list_of_lists = list(zip(*itertools.zip_longest(*[i.split(',') for i in data_dict[list_variable]],
                                                    fillvalue='')))
    new_col_names = ['{}_{}'.format(list_variable[:-1], i) for i in range(len(list_of_lists[0]))]
    for new_col_ind in range(len(new_col_names)):
        data_dict[new_col_names[new_col_ind]] = [i[new_col_ind] for i in list_of_lists]
    if delete_old_var:
        del data_dict[list_variable]
    return data_dict


def save_list_to_txt(list_of_vals, file_loc):
    """
    function to save python list to comma separated txt file for storage

    :param list_of_vals: python list
    :param file_loc: location and name of file
    :return: saves file to file_loc
    """
    with open(file_loc, 'w') as f:
        for element in list_of_vals:
            f.write("{}\n".format(element))


def read_txt_to_list(file_loc):
    """
    read .txt file in and return as list

    :param file_loc: location of txt file
    :return: list of file content
    """
    file = open(file_loc, 'r')
    lines = file.readlines()
    return lines
