"""
spider for scraping bank holidays uk

TODO - test attribute scrape
"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
import scrapy


class BankHolidayBaseSpider(AncestorSpider):

    def traverse_site(self, response):
        for year in range(2000, 2022):
            url = 'https://www.ukbankholidays.co.uk/year/{}'.format(str(year))
            yield scrapy.Request(url=url, callback=self.get_items)

    def get_items(self, response):
        holidays = "//ul[@class='calendar-items-list']/li"
        elements = [['country', 'div', 0, 'text'],
                    ['holiday', 'span', 0, 'text']]
        item_data = self.scrape_product_box(response, holidays, elements)
        item_data['holiday_date'] = self.scrape_to_attribute(response, holidays, 'text')
        self.validate_save_scraped_data(response.url, item_data, date_vars=True, attrs=False)
