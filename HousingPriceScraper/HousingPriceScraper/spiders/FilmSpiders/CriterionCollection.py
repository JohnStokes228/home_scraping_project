"""
spider for scraping criterion collections website for info on all their movies i guess

dont think the item scraper needs selenium

TODO - write attribute scrape
     - test attribute scrape
"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
import time
from random import randint


class CriterionCollectionBaseSpider(AncestorSpider):

    def get_items(self, response):
        self.requests.append(response.url)
        time.sleep(randint(3, 7))
        elements = [['spine_number', 'td', 0, 'text', {'class': 'g-spine'}],
                    ['title', 'td', 0, 'text', {'class': 'g-title'}],
                    ['director', 'td', 0, 'text', {'class': 'g-director'}],
                    ['country', 'td', 0, 'text', {'class': 'g-country'}],
                    ['year_of_release', 'td', 0, 'text', {'class': 'g-year'}]]
        item_data = self.scrape_product_box(response, '//tr[contains(@class, "gridFilm")]', elements)
        item_data['url'] = self.scrape_to_attribute(response, '//tr[@data-href]', 'data-href')
        self.update_urls_config(item_data['url'])
        self.validate_save_scraped_data(response.url, item_data, date_vars=True, attrs=False)
        self.responses.append(response.url)

