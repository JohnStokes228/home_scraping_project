"""
the next (final?) menu option to be added to the project, will include options for tracking content of logs
over time.

TODO - write method to highlight potential issues for select spiders
"""
import os
import json
from datetime import datetime
from HousingPriceScraper.HousingPriceScraper.functions.menus import basic_menu, basic_menu_non_functional
from HousingPriceScraper.HousingPriceScraper.functions.basic_functions import print_pizza_time
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
        print('Deleted selected log files')
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


def log_management_menu():
    """
    entry way into the wonderous world of my garbage low level logging.

    :return: it'll give you a menu to click through like the bitch you are
    """
    options_dict = {'highlight_issues': print_pizza_time,
                    'clean_logs': clear_logs}
    basic_menu(options_dict, back=True)
    return True
