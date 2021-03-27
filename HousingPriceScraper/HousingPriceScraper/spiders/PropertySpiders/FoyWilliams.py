"""
spider code for scraping Foy Williams' site. requires selenium to paginate, as urls are fragments only.

"""
import math
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Cephalothorax import PerceptiveAncestorSpider


class FoyWilliamsBaseSpider(PerceptiveAncestorSpider):

    def get_items(self, response):
        self.requests.append(response.url)
        self.get_url(response)
        number_of_properties = self.driver_scrape_to_attribute('//div/div/span[contains(@class,"pagination")]',
                                                               'text', multiple=False)
        number_of_pages = math.ceil(int(number_of_properties.split()[-1]) / 10)
        for i in range(1, (number_of_pages + 1)):
            elements = [["road", "//div[contains(@class,'address')]", "text"],
                        ["price", "//h4[contains(@class, 'price')]", "text"],
                        ["number_of_bedrooms", "//div[@class='row-fluid']/div/span[@class='bedNum']", "text"],
                        ["number_of_bathrooms", "//div[@class='row-fluid']/div/span[@class='bathNum']", "text"],
                        ["number_of_receptions", "//div[@class='row-fluid']/div/span[@class='receptNum']", "text"],
                        ["url", "//div/div/a[@href]", "href"]]
            data = self.driver_scrape_product_box("//div[contains(@id,'listing')]", elements)
            data['page_order'] = list(range(len(data['url'])))
            self.validate_save_scraped_data(response.url, data, date_vars=True)
            btn = self.find_press_button("(//li/a[@title='{}'])[1]".format(i+1))
            if not btn:
                break
        self.responses.append(response.url)