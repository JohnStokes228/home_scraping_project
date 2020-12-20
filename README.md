# home_scraping_project
home made web scraping project intended to allow for robust and scalable scraping of local housing market websites. 

current progress tracked at:
https://johnno.atlassian.net/jira/software/projects/WSH/boards/1

currently at v1, fairly happy with it here. theres deffo more that could be done but id rather that be informed by using it in situ for a bit and seeing what annoys me most rather than aribtrarily building from scratch.

to add a new spider:

- determine how deep into the website the spider needs to traverse, if it needs to crawl or can be put straight onto the page with data
- for each destinct action the spider takes (traverse, product data, attribute data) determine if selenium is required or if scrapy can be used raw
- build your spider inheriting from Ancestor Spider if no selenium is required, or from Perceptive Ancestor Spider if selenium is required.
- once spider is written, add some urls for it into default_urls.json
- create a new file in SpiderGroups folder, or add an instance of the spider into an existing one. this will attach the spider to a 'project'
- if you created a new spider group file above, it will need to be imported into scraping_main.py, and a new project will need to be added to the visible projects list.txt file
- hit play on the code, ensure the desired project is visible in the set visisble projects menu. set your chosen url config (reselect default here after every new spider is added).
- run the sider

once a spider has been run at product level, the 'recent_urls' config will populated with urls which can then feed an attribute level scrape if you select recent urls as the run_config of choice. config manager has many options on other basic commands for things you can do with recent urls such as creating wholly new configs out of them.
if you absolutely cant live with json data theres a data compilation module that can build a csv for you but Ive not tested it especially thoroughly and expect it will break since i don't personally see much use for it, its just there just in case.



