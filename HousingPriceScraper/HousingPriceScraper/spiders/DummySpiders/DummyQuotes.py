"""
file containing Dummy Quotes spider. I will test all future changes on this spider. includes immutable scrape,
addition of expanded list variables.

"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Cephalothorax import PerceptiveAncestorSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import expand_list_variable


class DummyQuotesBaseSpider(PerceptiveAncestorSpider):

    def get_items(self, response):

        self.requests.append(response.url)
        self.get_url(response)
        while True:
            elements = [("quote", "//div/span[@class='text']", "text"),
                        ("author", "//div/span/small", "text"),
                        ("tags", "//div/meta", "content")]
            test = self.driver_scrape_multiple_to_attribute(elements)
            test['page_order'] = list(range(len(test['quote'])))
            test = expand_list_variable(test, 'tags', delete_old_var=False)
            self.validate_save_scraped_data(response.url, test, date_vars=True)
            self.scroll_to_bottom()
            btn = self.find_press_button("//li[@class='next']/a[@href]")
            if not btn:
                break
        self.responses.append(response.url)
