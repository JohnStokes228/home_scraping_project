"""
functions used to store or interact with the data. currently includes date related functions too.

TODO - will eventually need to write a suite of functions to interact with data and its structures
"""
import os
from pathlib import Path
from datetime import date


def check_make_dir(folder):
    """
    checks if folder exists, and if not, creates it

    :param folder: folder to check for / makes name. accepts multiple layers
    :return: sticks the folder where the sun don't shine
    """
    base_directory = 'HousingPriceScraper/HousingPriceScraper/'
    if folder not in os.listdir(base_directory):
        Path('{}{}'.format(base_directory, folder)).mkdir(parents=True, exist_ok=True)
    print('directory ready at: \n{}{}'.format(base_directory, folder))


def date_today():
    """
    gets todays date in form ddmmyyyy. used in spider to make directory with specific name

    :return: string format date
    """
    today = date.today().strftime('%d%m%Y')
    return today
