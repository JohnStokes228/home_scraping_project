"""
file containing code for vodsmelee spider. used to get videos of gameplay for Will, but dont
run for fear of being blocked by youtube lol.

"""
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Cephalothorax import PerceptiveAncestorSpider
from HousingPriceScraper.HousingPriceScraper.spiders.AncestorSpider.Exoskeleton import AncestorSpider
import scrapy
from HousingPriceScraper.HousingPriceScraper.functions.data_management import check_make_dir


class VodsMeleeBaseSpider(PerceptiveAncestorSpider):

    def get_items(self, response):

        self.responses.append(response.url)
        self.get_url(response)

        while True:
            elements = [("tournament", "//tr/td[1]", "text"),
                        ("left_player", "//tr/td[2]/a/span/b[1]", "text"),
                        ("right_player", "//tr/td[2]/a/span/b[2]", "content"),
                        ("left_character", "//tr/td[2]/a/span/img[1]", "src"),
                        ("right_character", "//tr/td[2]/a/span/img[last()]", "src"),
                        ("video_url", "//tr/td[3]/a", "href"),
                        ("match_type", "//tr/td[4]", "text"),
                        ("round", "//tr/td[5]", "text")]
            #  left/right character don't allow players to have two characters which it looks like they sometimes can :O
            elements = self.driver_scrape_multiple_to_attribute(elements)
            elements['left_character'] = [character.split('-')[1].split('.')[0] for character in elements['left_character']]
            elements['right_character'] = [character.split('-')[1].split('.')[0] for character in elements['right_character']]
            self.validate_save_scraped_data(response.url, elements, date_vars=False)
            btn = self.find_press_button("//a[@title='Go to next page']", centralise=True)
            self.responses.append(response.url)
            if hasattr(self, 'get_attributes'):
                for url in elements['video_url']:
                    yield scrapy.Request(url=url, callback=self.get_attributes)
                    self.requests.append(url)
            if not btn:
                break


class VodsMeleeAttrSpider(AncestorSpider):

    def get_attributes(self, response):
        video_file = self.scrape_to_attribute(response, '///a[@aria-label="Watch on YouTube"]', 'href')
        check_make_dir(self.data_path+'/videos')
        self.scrape_video_to_mp4(video_file, self.data_path+'/videos')

