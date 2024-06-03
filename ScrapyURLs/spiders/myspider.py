from typing import Iterable
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MyspiderSpider(CrawlSpider):
    name = "myspider"
    # allowed_domains = ["localhost:700"]
    start_urls = ["http://localhost:700/index.html"]
    custom_settings = {
        'DEPTH_LIMIT': 1,  # Limit the depth to 1
    }

    # DEFAULT SCRAPY START FUNCTION - Override
    # iterates over 'start_urls' to generate HTTP 'Request' objects
    def start_requests(self):
        for url in self.start_urls:
            print('start_requests', 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
            print(url)
            yield scrapy.Request(url, callback=self.parse_link)

    # Dictionary to hold the parent-child relationships
    results = {}

    rules = (
        Rule(
            # allow=('\/.*',), 
            LinkExtractor(restrict_css='div.mwsbodytext ul li a'), # Extract links within specified CSS selector
            callback='parse_link', # Process each link with this method
            follow=False,
            process_request='process_request'  # Modify each (url extracted) request before sending (aka Crawling them)
        ),
    )

    def process_request(self, request, response):
        print('\nprocess_request', 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
        print(request.url, '\n', request.meta)
        request.meta['errback'] = self.handle_error   # what is meta 'errback' ? default recognized by scrapy ?
        print(request.url, '\n', request.meta, 'zzzzz\n')
        return request

    def handle_error(self, failure):
        pass

    def parse_link(self, response):
        parent_url = response.meta.get('parent_url', 'root')
        current_url = response.url

        print("\nparse_link aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(parent_url, current_url)
        # response.meta
        # {'rule': 0, 'link_text': 'Homepage, Link 3', 'depth': 1, 'download_timeout': 180.0, 'download_slot': 'localhost', 'download_latency': 0.00288}
        print(response.meta.get('zozo', 'link_text'),  'aaaa')
        print('\n\tHTTP: ', response.status, '\tURL: ', response.url, '\n')

        # Extract all links from the response
        links = response.css('a::attr(href)').getall()    # extract() vs. getall() ??
        for link in links:
            full_url = response.urljoin(link)
            # Check if the link is external (outside 'mysite.com')
            if not link.startswith('http://localhost:700'):
                # Yield a dictionary with the external URL and status code
                yield {
                    'urls_inside': full_url
                }
                # ask chatGPT to save 'referer' and parent-child ; Crawled (for URLs) vs. Scraped (data requested)


