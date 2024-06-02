import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MyspiderSpider(CrawlSpider):
    name = "myspider"
    # allowed_domains = ["localhost:700"]
    start_urls = ["http://localhost:700/index.html"]
    custom_settings = {
        'DEPTH_LIMIT': 2,  # Limit the depth to 1
    }

    rules = (
        Rule(
            # allow=('\/.*',), 
            LinkExtractor(restrict_css='div.mwsbodytext ul li'), 
            callback='parse_item', 
            follow=True),
    )

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


