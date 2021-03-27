"""
file containing generic small functions which may get used throughout the project, to improve readability of
files which utilise them. this files necessity is a product of my love of micro functions maybe i should consider
toning it down...?

"""
import string
import itertools
from datetime import date, datetime


def print_pizza_time():
    """
    function prints the words 'pizza time!' to trace.

    :return: pizza time!
    """
    print('pizza time!\n')
    return True


def date_today():
    """
    gets todays date in form ddmmyyyy. used in spider to make directory with specific name

    :return: string format date
    """
    today = date.today().strftime('%d%m%Y')
    return today


def current_time():
    """
    gets the current time in form hhmmss. used to identify individual jsons in the data files.

    :return: string format time
    """
    now = datetime.now().time().strftime('%H%M%S')
    return now


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
