"""
spider for scraping criterion collections website for info on all their movies i guess

dont think the item scraper needs selenium

TODO - test attribute scrape
"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Cephalothorax import PerceptiveAncestorSpider
from HousingPriceScraper.HousingPriceScraper.functions.basic_functions import alphabet_list_length
import time
from random import randint
import scrapy


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
        self.validate_save_scraped_data(response.url, item_data, date_vars=False, attrs=False)
        self.responses.append(response.url)
        if hasattr(self, 'get_attributes'):
            for url in item_data['url']:
                yield scrapy.Request(url=url, callback=self.get_attributes)
                self.requests.append('http://books.toscrape.com/catalogue/{}'.format(url))


class CriterionCollectionAttrSpider(AncestorSpider):

    def get_attributes(self, response):

        self.requests.append(response.url)
        time.sleep(randint(2, 6))
        elements = [('blurb', '//div[@class="product-summary"]/p', 'text'),
                    ('run_time', '(//ul[@class="film-meta-list"]/li)[4]', 'text'),
                    ('colour', '(//ul[@class="film-meta-list"]/li)[5]', 'text'),
                    ('aspect_ratio', '(//ul[@class="film-meta-list"]/li)[6]', 'text'),
                    ('language', '(//ul[@class="film-meta-list"]/li)[7]', 'text'),
                    ('formats', '//span[@class="meta-item"]/span[@class="item"]', 'text'),
                    ('cast', '(//dl[@class="creditList"])[1]/dt', 'text'),
                    ('credits', '(//dl[@class="creditList"])[2]', 'text'),
                    ('special_features', '//div[@class="product-features-list"]/ul/li', 'text')]
        attribute_data = self.scrape_multiple_to_attribute(response, elements)
        attribute_data['url'] = [response.url]
        self.validate_save_scraped_data(response.url, attribute_data, date_vars=False, attrs=True)
        self.responses.append(response.url)


class CriterionReviewSpider(PerceptiveAncestorSpider):

    def traverse_site(self, repsonse):

        alphabet = alphabet_list_length(26)
        alphabet = [letter.upper() for letter in alphabet]
        for letter in alphabet:
            url = 'https://www.criterionforum.org/Reviews/{}'.format(letter)
            yield scrapy.Request(url=url, callback=self.get_items)
            self.requests.append('https://www.criterionforum.org/Reviews/{}'.format(letter))
        yield scrapy.Request(url='https://www.criterionforum.org/Reviews/', callback=self.get_items)

    def get_items(self, response):

        self.requests.append(response.url)
        self.get_url(response)
        time.sleep(randint(4, 8))
        elements = [('title', '//span[@data-bind="text: Title"]', 'text'),
                    ('company', '//div[@data-bind="text: SeriesType"]', 'text'),
                    ('year_of_disk_release', '//td[@data-bind and @class="info"]', 'text'),
                    ('scores', '//td[@data-bind="text: Grades()"]', 'text')]
        review_data = self.driver_scrape_multiple_to_attribute(elements)
        review_data['year_of_disk_release'] = [year.split(',')[-1] for year in review_data['year_of_disk_release']]
        review_data['picture_score'] = [score.split('/')[0] for score in review_data['scores']]
        review_data['audio_score'] = [score.split('/')[1] for score in review_data['scores']]
        review_data['extras_score'] = [score.split('/')[2] for score in review_data['scores']]
        self.validate_save_scraped_data(response.url, review_data, date_vars=False, attrs=False)
        self.responses.append(response.url)