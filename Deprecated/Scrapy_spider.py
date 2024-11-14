# Imports

import scrapy
from scrapy.crawler import CrawlerProcess

# spider class definition

class ImmoSpider(scrapy.Spider):

    name = "immo_spider"

    def start_requests(self):
        urls = ['https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page=1&orderBy=relevance'] # Fill the url obtained from selenium for refined search list
        for url in urls:
            yield scrapy.Request(url= url, callback= self.parse_list_pages)

    def parse_list_pages(self, response):
        listing_links = response.xpath('//li[@class="search-results_item"]//hs/a/@href').extract()
        for link in page_links:
            yield response.follow(url = link, callback= self.parse_listings)

    def parse_listings(self, response):
        


# Running the spider

process = CrawlerProcess() # Initiate crawler process
process.crawl(ImmoSpider) # Which spider to use?
process.start() # Start crawling