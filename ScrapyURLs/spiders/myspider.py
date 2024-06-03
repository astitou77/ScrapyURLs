import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MyspiderSpider(CrawlSpider):
    name = "myspider"
    # allowed_domains = ["localhost:700"]
    start_urls = ["http://localhost:700/index.html"]
    custom_settings = {
        'DEPTH_LIMIT': 4,  # Limit the depth to 1
    }

    # Dictionary to hold the parent-child relationships
    results = {}

    rules = (
        Rule(
            # allow=('\/.*',), 
            LinkExtractor(restrict_css='div.mwsbodytext ul li'), # Extract links within specified CSS selector
            callback='parse_item', # Process each link with this method
            follow=True
        ),
    )

    def process_request(self, request, response):
        request.meta['errback'] = self.handle_error
        pass

    def parse_item(self, response):
        # Extract all links from the response
        links = response.css('a::attr(href)').extract()
        for link in links:
            full_url = response.urljoin(link)
            status = response.status
            # Check if the link is external (outside 'mysite.com')
            if not link.startswith('http://localhost:700'):
                # Yield a dictionary with the external URL and status code
                yield {
                    'url': full_url,
                    'status': status  # Set status to None for external links
                }


