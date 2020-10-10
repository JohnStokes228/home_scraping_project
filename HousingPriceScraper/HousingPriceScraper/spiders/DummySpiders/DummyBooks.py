"""
file containing code for Dummy Books Spider. currently being used to test the various methods rather than utilising a
live site.

TODO - write method to test css
     - determine if its possible to interact for instance with pagination buttons without use of a driver.
     - books will instead produce its url hit list via pattern from url
"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import save_dict_to_json


class DummyBooksBaseSpider(AncestorSpider):

    def parse(self, response):

        elements = [['name', 'a', 1, 'title'],
                    ['price', 'p', 0, 'text', {'class': 'price_color'}],
                    ['url', 'a', 1, 'href']]
        test = self.scrape_product_box(response, '//article', elements)
        test['page_order'] = list(range(len(test['name'])))
        save_dict_to_json(test, self.data_path, self.name)
