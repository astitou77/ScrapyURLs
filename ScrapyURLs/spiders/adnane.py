import scrapy


class AdnaneSpider(scrapy.Spider):
    name = "adnane"
    allowed_domains = ["adnane.com"]
    start_urls = ["https://adnane.com"]

    def parse(self, response):
        pass
