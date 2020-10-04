"""
file containing code for Dummy Books Spider. currently being used to test the various methods rather than utilising a
live site.

TODO - write method to test css
     - determine if its possible to interact for instance with pagination buttons without use of a driver.
"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import date_today


class DummyBooksSpider(AncestorSpider):

    name = 'dummy-books'
    input_urls = ['http://books.toscrape.com/']
    data_path = 'data/raw_data/dummy_data/{}/{}'.format(name, date_today())

    def parse(self, response):

        elements = [('name', '//h3/a', 'title'),
                    ('price', '//div/p[@class="price_color"]', 'text'),
                    ('url', '//h3/a', 'href')]
        test = self.scrape_multiple_to_attribute(response, elements)

        elements2 = [['name', 'a', 1, 'title'],
                     ['price', 'p', 0, 'text', {'class': 'price_color'}],
                     ['url', 'a', 1, 'href']]
        test2 = self.scrape_product_box(response, '//article', elements2)

        print(test)
        print(test2)
