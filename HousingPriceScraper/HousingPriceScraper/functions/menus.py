"""
contains generic code for use in main menus. currently this is a function which turns dictionaries of functions
into a menu. I envision any further menu functions being stored here so don't expect it to run like a pipeline but
rather like a suite of individual menus.

TODO - write a method that utilises the back button to properly test it
     - it may be that some of these functions end up elsewhere as I can see end_process being useful...
"""


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
