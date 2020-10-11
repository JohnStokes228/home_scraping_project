"""
file containing Dummy Quotes spider. I will test all future changes on this spider. includes immutable scrape,
addition of expanded list variables.

TODO - spider will paginate using some kind of intelligent method, as opposed to books which will use
       cheeky pattern spotting for this purpose
"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
from HousingPriceScraper.HousingPriceScraper.functions.data_management import save_dict_to_json, expand_list_variable


class DummyQuotesBaseSpider(AncestorSpider):

    def get_items(self, response):

        elements = [("quote", "//div/span[@class='text']", "text"),
                    ("author", "//div/span/small", "text"),
                    ("tags", "//div/meta", "content")]
        test = self.scrape_multiple_to_attribute(response, elements)
        test['page_order'] = list(range(len(test['quote'])))
        test = expand_list_variable(test, 'tags', delete_old_var=False)
        save_dict_to_json(test, self.data_path, self.name)
