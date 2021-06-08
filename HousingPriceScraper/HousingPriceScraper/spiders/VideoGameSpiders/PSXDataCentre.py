"""
Spider for scraping the psx data centre for playstation 1 game information.
"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
import scrapy


class PSXDataCentreBaseSpider(AncestorSpider):

    def traverse_site(self, response):
        target_xpath = "//tbody/tr/td[@class='col1']/a[@target='plist']"
        sub_domains = self.scrape_to_attribute(response, target_xpath, 'href')

        for domain in sub_domains:
            url = "https://psxdatacenter.com/{}".format(domain)
            yield scrapy.Request(url=url, callback=self.get_items)

    def get_items(self, response):
        pass