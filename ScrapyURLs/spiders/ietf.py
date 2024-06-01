import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class IetfSpider(scrapy.Spider):
    name = 'ietf'
    allowed_domains = ['www.canada.ca']
    start_urls = ['https://www.canada.ca/en/department-national-defence/corporate/policies-standards/defence-administrative-orders-directives/1000-series.html']
    custom_settings = {
        'DEPTH_LIMIT': 3,  # Change the depth limit as needed
    }

    rules = (
        Rule(LinkExtractor(restrict_css='div.mwsbodytext a'), callback='parse', follow=True),
    )

    def parse(self, response):
        # Extract the URL and status code from the response
        url = response.url
        status = response.status
        # Yield a dictionary with URL and status code
        yield {
            'url': url,
            'status': status
        }