"""
file containing Dummy Quotes spider. I will test all future changes on this spider. includes immutable scrape,
addition of expanded list variables.

TODO - write some kind of attribute method to test how multiple drivers works as I think its possible
       that there might be some messiness involved with that. it could just use the one parents driver
       but it needs to be tested to be sure.

"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Cephalothorax import PerceptiveAncestorSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import save_dict_to_json, expand_list_variable


class DummyQuotesBaseSpider(PerceptiveAncestorSpider):

    def get_items(self, response):

        self.get_url(response)
        elements = [("quote", "//div/span[@class='text']", "text"),
                    ("author", "//div/span/small", "text"),
                    ("tags", "//div/meta", "content")]
        test = self.scrape_multiple_to_attribute(response, elements)
        self.driver_get_element("//div/span[@class='text']")
        test['page_order'] = list(range(len(test['quote'])))
        test = expand_list_variable(test, 'tags', delete_old_var=False)
        save_dict_to_json(test, self.data_path, self.name)
