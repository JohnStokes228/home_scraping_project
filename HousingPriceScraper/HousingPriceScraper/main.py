"""
Uncle Johnnos' Scraping Project.
Inspired by the other one, though hopefully with some improvements to the design as and when i get to them.
I've decided to keep this file as clean as possible for legibility reasons / because most of what belongs in it is
generic code i also want to use elsewhere. This decision also allows us to delay the activation of the reactor until
such a time as it is unavoidable, thus dodging any nuisance that that usually causes.

TODO - add new options: consolidate_data
     - add new option: get_log_summary
     - add new option: print_pizza_time for nostalgia's sake
"""
from HousingPriceScraper.HousingPriceScraper.functions.menus import basic_menu
from HousingPriceScraper.HousingPriceScraper.processes.run_scrapers import run_scrapers


if __name__ == '__main__':
    options_dict = {'run_scrape': run_scrapers}
    basic_menu(options_dict)
