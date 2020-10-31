"""
the shared memory of the spiders. My intention is to have a single, cleanable log per spider but we'll see how that
goes. I wonder if QAing functions should be covered here too? Yes, yes they should

TODO - write method to create new log file if needed
     - write methods to update logs with info on pass / fail of variable lengths
     - write method to update logs with info on pass / fail of NULL checks
     - write method to update logs with number of pages produced
     - write method to update logs with number (and specifics) of urls from input list not scraped
     - write method to update log file for spider with todays info.
"""
from HousingPriceScraper.HousingPriceScraper.functions.basic_functions import date_today
import os
import json


class HiveMind:

    run_log = {date_today(): {'no_length_fails': 0,
                              'no_NULL_fails': 0,
                              'no_runs': 0,
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
            return None

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

    def save_log(self):
        pass
