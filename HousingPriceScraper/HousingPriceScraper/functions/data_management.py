"""
functions used to store or interact with the data. currently includes date related functions too.

TODO - will eventually need to write a suite of functions to interact with data and its structures
"""
from pathlib import Path
from datetime import date


def check_make_dir(folder):
    """
    checks if folder exists, and if not, creates it

    :param folder: folder to check for / makes name. accepts multiple layers
    :return: sticks the folder where the sun don't shine
    """
    Path('{}'.format(folder)).mkdir(parents=True, exist_ok=True)
    print('directory ready at {}'.format(folder))


def date_today():
    """
    gets todays date in form ddmmyyyy. used in spider to make directory with specific name

    :return: string format date
    """
    today = date.today().strftime('%d%m%Y')
    return today
