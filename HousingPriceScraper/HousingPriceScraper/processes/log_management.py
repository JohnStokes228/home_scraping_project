"""
the next (final?) menu option to be added to the project, will include options for tracking content of logs
over time.

"""
import os
import json
from datetime import datetime
from statistics import mean
from math import ceil
from HousingPriceScraper.HousingPriceScraper.functions.menus import basic_menu, basic_menu_non_functional
from HousingPriceScraper.HousingPriceScraper.processes.run_scrapers import find_visible_projects


def get_select_log_files():
    """
    function finds all logs associated to the spiders chosen by the user.

    :return: list of chosen log files
    """
    visible_projects = find_visible_projects()
    datas = []
    for project in visible_projects:
        project_data = os.listdir('HousingPriceScraper/HousingPriceScraper/data/raw_data/{}'.format(project))
        datas += ['{}/{}'.format(project, i) for i in project_data]
    chosen_datas = basic_menu_non_functional([i.split('/')[1] for i in datas])
    logs_list = os.listdir('HousingPriceScraper/HousingPriceScraper/data/scrape_logs')
    logs_list = [file for file in logs_list for log in chosen_datas if log in file]
    return logs_list


def keep_most_recent():
    """
    reads in log files and removes all but most recent data. for now we'll keep only the most recent date but prehaps
    in future this could change depending on what seems most useful

    :return: updates selected logs in data/scrape_logs
    """
    logs_to_clean = get_select_log_files()
    if len(logs_to_clean) > 0:
        for log in logs_to_clean:
            with open('HousingPriceScraper/HousingPriceScraper/data/scrape_logs/{}'.format(log)) as log_json:
                log_dict = json.load(log_json)
            dates = [datetime.strptime(date, '%d%m%Y') for date in log_dict.keys()]
            max_date = max(dates).strftime('%d%m%Y')
            log_dict = {max_date: log_dict[max_date]}
            with open('HousingPriceScraper/HousingPriceScraper/data/scrape_logs/{}'.format(log), 'w') as fp:
                json.dump(log_dict, fp, sort_keys=True, indent=4)
            print('Updated file {}, file now includes only log for date {}'.format(log, max_date))
    else:
        print('No logs for selected spiders are available to clean')
    return True


def delete_oldest():
    """
    reads in and removes the oldest log information from selected logs

    :return: updates selected logs in data/scrape_logs
    """
    logs_to_clean = get_select_log_files()
    if len(logs_to_clean) > 0:
        for log in logs_to_clean:
            with open('HousingPriceScraper/HousingPriceScraper/data/scrape_logs/{}'.format(log)) as log_json:
                log_dict = json.load(log_json)
            dates = [datetime.strptime(date, '%d%m%Y') for date in log_dict.keys()]
            min_date = min(dates).strftime('%d%m%Y')
            del log_dict[min_date]
            with open('HousingPriceScraper/HousingPriceScraper/data/scrape_logs/{}'.format(log), 'w') as fp:
                json.dump(log_dict, fp, sort_keys=True, indent=4)
            print('Updated file {}, file no longer includes log information for {}'.format(log, min_date))
    else:
        print('No logs for selected spiders are available to clean')
    return True


def full_cleanse():
    """
    fully delete logs for select spiders. no going back with this method!!!

    :return: deletes chosen files from scrape_logs folder
    """
    logs_to_delete = get_select_log_files()
    if len(logs_to_delete) > 0:
        for log in logs_to_delete:
            os.remove('HousingPriceScraper/HousingPriceScraper/data/scrape_logs/{}'.format(log))
            print('Deleted file {}'.format(log))
    else:
        print('No logs to delete for chosen selection')
    return True


def clear_logs():
    """
    function for clear_logs menu

    :return: entryway into clear logs menu
    """
    options_dict = {'keep_most_recent_info': keep_most_recent,
                    'delete_oldest_info': delete_oldest,
                    'delete_logs': full_cleanse}
    basic_menu(options_dict, back=True)
    return True


def get_average(log_dict, numeric_var, max_date):
    """
    dictionary gets average of numeric variable not including most recent value

    :param log_dict: dictionary of dated logs
    :param numeric_var: the numeric variable to be compared
    :param max_date: the maximum date key for log_dict
    :return: integer difference between recent value and average
    """
    past_vals = [ceil(log_dict[date][numeric_var] / log_dict[date]['no_runs']) for date in log_dict.keys() if date != max_date]
    if len(past_vals) > 1:
        mean_past_vals = mean(past_vals)
    elif len(past_vals) == 1:
        mean_past_vals = past_vals[0]
    else:
        mean_past_vals = 0
    return ceil(mean_past_vals)


def highlights():
    """
    highlight issues from recent run

    :return: probably prints some info of interest
    """
    logs_to_check = get_select_log_files()
    if len(logs_to_check) > 0:
        for log in logs_to_check:
            with open('HousingPriceScraper/HousingPriceScraper/data/scrape_logs/{}'.format(log)) as log_json:
                log_dict = json.load(log_json)
            print('\nLOG {}:'.format(log.replace('.json', '')))
            dates = [datetime.strptime(date, '%d%m%Y') for date in log_dict.keys()]
            max_date = max(dates).strftime('%d%m%Y')
            min_date = min(dates).strftime('%d%m%Y')
            print('The most recent run for this spider occurred on {}, when {} runs occurred'.format(max_date, log_dict[max_date]['no_runs']))
            if log_dict[max_date]['no_length_fails'] != 0:
                print('There were {} instances of mismatched variable lengths during runs on this date'.format(log_dict[max_date]['no_length_fails']))
            if log_dict[max_date]['no_NULL_fails'] != 0:
                print('{} pages scraped yielded at least one NULL value during runs on this date'.format(log_dict[max_date]['no_NULL_fails']))
            if len(log_dict[max_date]['missed_urls']) != 0:
                print('There were {} requested urls which yielded no response during runs on this date'.format(len(log_dict[max_date]['missed_urls'])))
            movement = get_average(log_dict, 'no_pages_scraped', max_date)
            print('The most recent run on {} scraped {} pages, compared to a historic average of {}'.format(max_date, log_dict[max_date]['no_pages_scraped'], movement))
            if len(dates) > 1:
                previous_date = sorted(dates)[-2].strftime('%d%m%Y')
                print('The second most recent run on {} scraped {} pages'.format(previous_date, log_dict[previous_date]['no_pages_scraped']))
            print('The earliest recorded run on {} scraped {} pages'.format(min_date, log_dict[min_date]['no_pages_scraped']))
    else:
        print('No logs to check for selected spiders!')
    print('\n')
    return True


def log_management_menu():
    """
    entry way into the wonderous world of my garbage low level logging.

    :return: it'll give you a menu to click through like the bitch you are
    """
    options_dict = {'highlight_issues': highlights,
                    'clean_logs': clear_logs}
    basic_menu(options_dict, back=True)
    return True
