# home_scraping_project

home made web scraping project initially designed for scraping house prices (hence all the project names) however they mostly block scrapers from those sites and i dont want to be too norty at the moment so its barely been used for this purpose. instead, I've been using it to fuel my other projects. The code is a bit of a toy in that its full of (terribly written) text menus with loads of options that probably just wont get used but it was a fun and educational experience to build from scratch so ack well. 

current progress tracked at:
https://johnno.atlassian.net/jira/software/projects/WSH/boards/1

currently at v1, and waiting until its been used enough to determine what the most important next steps might be. most up to date branch is called 'V2_branch', I have no idea why. seems like the sort of joke I'd make though doesnt it. 
  
# To set up a new scraper

- create a spider in the spiders folder, it should inherit from either AncestorSpider, or, if it requires JavaScript interaction, PerceptiveAncestorSpider.
- add a key / url list for the spider to configs/input_urls/defaults. you may also wish to add alternate configs either to existing config jsons, or create an entirely new one.
- in 'SpiderGroups' folder, either create a new group or append your spider to an existing group. A new group should include a group_path variable to dictate where data from that groups spiders are saved.
- make sure that the group file your spider is in is imported into processes/run_scrapers
- when running the code be sure to set the available projects to include you current SpiderGroups, and be sure to select your URL configs - the new spider will not have any URLS unless you do this even if you only want to run default options

your spider should then be ready to run.

# config options

# post scrape validation

 



