"""
file containing code for Dummy Books Spider. currently being used to test the various methods rather than utilising a
live site.

TODO - write method to test css
"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import save_dict_to_json
import scrapy


class DummyBooksBaseSpider(AncestorSpider):

    def traverse_site(self, response):

        pagination_information = self.scrape_to_attribute(response, '//form/strong', 'text')
        number_of_pages = int(pagination_information[0]) / int(pagination_information[2])
        for i in range(1, int(number_of_pages)):
            yield scrapy.Request('http://books.toscrape.com/catalogue/page-{}.html'.format(str(i)),
                                 callback=self.get_items)

    def get_items(self, response):

        elements = [['name', 'a', 1, 'title'],
                    ['price', 'p', 0, 'text', {'class': 'price_color'}],
                    ['url', 'a', 1, 'href']]
        test = self.scrape_product_box(response, '//article', elements)
        test['page_order'] = list(range(len(test['name'])))
        self.update_recent_urls(['http://books.toscrape.com/catalogue/{}'.format(url) for url in test['url']])
        save_dict_to_json(test, self.data_path, self.name)
        if hasattr(self, 'get_attributes'):
            for url in test['url']:
                yield scrapy.Request(url='http://books.toscrape.com/catalogue/{}'.format(url), callback=self.get_attributes)


class DummyBookAttrSpider(AncestorSpider):

    def get_attributes(self, response):

        elements = [('name', '//div/h1', 'text'),
                    ('description', '(//p)[4]', 'text')]
        test = self.scrape_multiple_to_attribute(response, elements)
        attrs = self.scrape_table_to_dict(response, '//th', 'text', '//td', 'text')
        test.update(attrs)
        save_dict_to_json(test, self.data_path, format(self.name), attrs=True)
