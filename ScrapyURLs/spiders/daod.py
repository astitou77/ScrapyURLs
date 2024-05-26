import scrapy


class DaodSpider(scrapy.Spider):
    name = "daod"
    allowed_domains = ["www.canada.ca"]
    start_urls = ["https://www.canada.ca/en/department-national-defence/corporate/policies-standards/defence-administrative-orders-directives/1000-series.html"]

    def parse(self, response):
        pass