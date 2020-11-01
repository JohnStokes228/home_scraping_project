"""
the shared memory of the spiders. My intention is to have a single, cleanable log per spider but we'll see how that
goes. I wonder if QAing functions should be covered here too? Yes, yes they should

TODO - write method to update logs with number (and specifics) of urls from input list not scraped
"""
from HousingPriceScraper.HousingPriceScraper.functions.basic_functions import date_today
from HousingPriceScraper.HousingPriceScraper.functions.data_management import merge_dictionaries
import os
import json


class HiveMind:

    scrape_log = {date_today(): {'no_length_fails': 0,
                                 'no_NULL_fails': 0,
                                 'no_runs': 0,
                                 'no_response_urls': 0,
                                 'no_request_urls': 0,
                                 'missed_urls': [],
                                 'no_pages_scraped': 0}}

    def get_log(self):
        """
        checks for the existance of a log file for a given spider and reads it in if needed

        :return: either None or a dictionary
        """
        logs = os.listdir('data/scrape_logs')
        logs = [log for log in logs if self.name in log]
        if len(logs) > 0:
            with open(logs[0]) as current_log_file:
                spider_log = json.load(current_log_file)
            return spider_log
        else:
            return False

    def check_log_for_today(self, log):
        """
        check if log file already has an entry for today

        :param log: a json dictionary
        :return: True if True, False if not. big shocker that ey
        """
        if date_today() in log.keys():
            return True
        else:
            return False

    def variable_length_check(self, data_dict, url):
        """
        checks if number of attributes scraped is equal across the board

        :param url: the url scraped
        :param data_dict: dictionary of scraped data
        :return: True if pass, else False
        """
        lengths = [len(value) for value in data_dict.values()]
        if len(set(lengths)) == 1:
            print('LOGGER PASS: successfully scraped {} values from:\n\t{}'.format(lengths[0], url))
            return True
        else:
            print('LOGGER FAIL: number of attributes per variable is inconsistent from url:\n{}'.format(url))
            self.scrape_log[date_today()]['no_length_fails'] += 1
            return False

    def null_value_check(self, data_dict):
        """
        checks for NULLs within scraped data, returns False if present

        :param data_dict: dictionary of scraped data
        :return: True if pass, False if fail
        """
        start_nulls = self.scrape_log[date_today()]['no_NULL_fails']
        for key in data_dict.keys():
            if None in data_dict[key]:
                print('LOGGER FAIL: found NoneTypeObj in variable {}'.format(key))
                self.scrape_log[date_today()]['no_NULL_fails'] += 1
        if start_nulls == self.scrape_log[date_today()]['no_NULL_fails']:
            print('LOGGER PASS: no NULLs present in data')
            return True
        else:
            return False

    def increment_numeric(self, numeric='no_pages_scraped'):
        """
        increment numeric value in log dictionary

        :param numeric: name of numeric variable to increment
        :return: increments don't you get it
        """
        self.scrape_log[date_today()][numeric] += 1
        print('LOGGER: added 1 to {}'.format(numeric))

    def response_url_check(self):
        """
        check the requests sent verse responses received

        :return:
        """
        self.scrape_log[date_today()]['no_response_urls'] = len(self.responses)
        self.scrape_log[date_today()]['no_request_urls'] = len(self.requests)
        self.scrape_log[date_today()]['missed_urls'] = [i for i in self.requests if i not in self.responses]
        if len(self.scrape_log[date_today()]['missed_urls']) > 0:
            print('LOGGER FAIL: there were {} urls not successfully scraped, including:')
            for url in self.scrape_log[date_today()]['missed_urls']:
                print('\t- {}'.format(url))
        else:
            print('LOGGER PASS: all requests yielded data')

    def save_log(self):
        """
        reads in existing log, appends self.log to it, saves it to logs folder

        :return: saves json log like a big tiddy bitch
        """
        self.increment_numeric('no_runs')
        self.response_url_check()
        log_info = self.scrape_log
        existing_log = self.get_log()
        if type(existing_log) == 'dict':
            if not self.check_log_for_today():
                log_info.update(existing_log)
            else:
                log_info = merge_dictionaries([log_info, existing_log])
        with open('data/scrape_logs/{}.json'.format(self.name), 'w') as fp:
            json.dump(log_info, fp, sort_keys=True, indent=4)
