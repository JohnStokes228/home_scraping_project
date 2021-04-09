"""
spider for scraping wikipedia.com. Apparently they allow bot access so long as its not too fast, so keep it slowww,
theres only a few tables we really need anyways. I'm only scraping the 'debuted' fighters list for the country of origin
as the rest of them arent likely to have any fights listed yet. I'm also not yet sure how useful the camp spider will
be as it only has a few fighters camps not the whole shebang. ack well lad lets see what happens I guess

"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
import time
from random import randint
import scrapy

class WikipediaCampBaseSpider(AncestorSpider):

    def get_items(self, response):
        self.requests.append(response.url)
        time.sleep(randint(3, 7))

        elements = [('camp', '//table[@class="wikitable"]/tbody/tr/td[1]', 'text'),
                    ('coaches', '//table[@class="wikitable"]/tbody/tr/td[2]', 'text'),
                    ('current_fighters', '//table[@class="wikitable"]/tbody/tr/td[3]', 'text'),
                    ('previous_fighters', '//table[@class="wikitable"]/tbody/tr/td[4]', 'text'),
                    ('camp_location', '//table[@class="wikitable"]/tbody/tr/td[5]', 'text')]
        attribute_data = self.scrape_multiple_to_attribute(response, elements)
        self.validate_save_scraped_data(response.url, attribute_data, date_vars=False, attrs=True)
        self.responses.append(response.url)


class WikipediaFighterBaseSpider(AncestorSpider):

    def get_items(self, response):
        self.requests.append(response.url)
        time.sleep(randint(3, 7))

        elements = [('country_of_origin', '//table[position() > 7]/tbody/tr/td/img', 'alt'),
                    ('fighter', '(//table[position() > 7]/tbody/tr)/td[2]', 'text')]
        attribute_data = self.scrape_multiple_to_attribute(response, elements)
        self.validate_save_scraped_data(response.url, attribute_data, date_vars=False, attrs=True)
        self.responses.append(response.url)