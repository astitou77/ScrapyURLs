import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MyspiderSpider(CrawlSpider):
    name = "myspider"
    allowed_domains = ["www.canada.ca"]
    start_urls = ["https://www.canada.ca/en/department-national-defence/corporate/policies-standards/defence-administrative-orders-directives.html"]
    custom_settings = {
        'DEPTH_LIMIT': 1,  # Limit the depth to 1
    }

    rules = (
        Rule(
            # allow=('\/.*',), 
            LinkExtractor(restrict_css='div.mwsbodytext'), 
            callback='parse_item', 
            follow=True),
    )

    def parse_item(self, response):
        # Extract all links from the response
        links = response.css('a::attr(href)').extract()
        for link in links:
            full_url = response.urljoin(link)
            # Check if the link is external (outside 'mysite.com')
            if not link.startswith('https://www.canada.ca'):
                # Yield a dictionary with the external URL and status code
                yield {
                    'url': full_url,
                    'status': None  # Set status to None for external links
                }
            else:
                # Follow internal links within the specified path
                yield scrapy.Request(link, callback=self.parse_item)

        # Extract the URL and status code from the response
        url = response.url
        status = response.status
        # Yield a dictionary with URL and status code
        yield {
            'url': url,
            'status': status
        }

