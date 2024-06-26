from typing import Iterable
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class MyspiderSpider(CrawlSpider):

    # PREDEFINED ATTRIBUTE
    # 'name' : identify the spider when running it from the command line
    # --------------------------------------------------------------------------------------------------
    name = "myspider"

    # PREDEFINED ATTRIBUTE
    # 'start_urls' : A list of URLs to start crawling from. 
    #                If start_requests is not defined, Scrapy generates requests for these URLs.
    # --------------------------------------------------------------------------------------------------
    start_urls = ["http://localhost:700/index.html"]

    # PREDEFINED ATTRIBUTE
    # 'allowed_domains' : A list of domains that the spider is allowed to crawl (download HTML content). 
    #                     Requests to URLs outside these domains will be ignored.
    # --------------------------------------------------------------------------------------------------
    allowed_domains = ["localhost"]

    # PREDEFINED ATTRIBUTE
    # 'custom_settings' : A dictionary of settings specific to this spider. 
    #                    These settings override the project-wide settings.
    # --------------------------------------------------------------------------------------------------
    custom_settings = {
        'DEPTH_LIMIT': 0,  # Limit the depth to 1
        # 'USER_AGENT': 'my-custom-user-agent',
    }

    # PREDEFINED ATTRIBUTE - for 'CrawlSpider' - not 'scrapy.Spider'
    # 'rule' : Defines a set of rules to follow links and extract data. 
    #          Each rule is an instance of 'Rule', which defines how to follow links and what callbacks to use.
    # 
    #   'LinkExtractor' : Used to specify which links to extract based on URL patterns, domains, XPath, or CSS selectors.
    #           'allow'           : A regular expression (or list of regexes) that the URLs must match to be extracted.
    #           'deny'            : A regular expression (or list of regexes) that the URLs must not match to be extracted.
    #           'allow_domains'   : A list of domains that the URLs must belong to be extracted.
    #           'deny_domains'    : A list of domains that the URLs must not belong to be extracted.
    #           'restrict_xpaths' : An XPath (or list of XPaths) to restrict the part of the page where the links should be extracted from.
    #           'restrict_css'    : A CSS selector (or list of selectors) to restrict the part of the page where the links should be extracted from.
    #   'callback'      : Method to be called with the response of each link extracted.
    #   'follow'        : Boolean indicating whether to continue following links from the pages downloaded using this rule.
    # --------------------------------------------------------------------------------------------------
    rules = (
        Rule(
            # start_requests='start_requests',  # default function, generates HTTP 'Requests' from start_urls[]
            LinkExtractor(restrict_css='div'), # Extract links within specified CSS selector  # allow=('\/.*',), 
            callback='parse_link', # Process each link with this method
            errback='parse_err_link',
            follow=True,
            process_request='process_request'  # Modify each (url extracted) request before sending (aka Crawling them)
        ),
    )

    # Dictionary to hold the parent-child relationships of URLs Scraped from Crawled URLs
    results = {}


    # PREDEFINED METHOD
    # 'start_requests' : Generates the initial requests to begin the crawling process. 
    #                    If not defined, Scrapy uses the start_urls attribute to create these requests.
    # --------------------------------------------------------------------------------------------------
    def start_requests_NOT_USED(self):
        for url in self.start_urls:
            print('start_requests', '0000000000000000000000000000000000000000000000000000000000000')
            print(url)

            # PREDEFINED
            # 'logger' : A Python logger instance for logging messages. 
            #            This is more flexible and recommended over the log method.
            # ------------------------------------------------------------------------------------------
            # self.logger.info('This is an info message')

            # PREDEFINED 'REQUEST' parameters - Crawls each start_urls, and sends HTML to be parsed.
            # 'callback' :  Specifies the method to be called with the response of the request.
            # 'errback'  :  Specifies the method to be called if an error occurs during the request.
            # 'meta'     :  A dictionary of metadata to be passed along with the request. 
            #               This can include custom data and control information.
            #               Ex.: yield scrapy.Request(url, callback=self.parse, errback=self.handle_error, meta={'depth': 1})
            # 'headers'  :  Allows you to set custom headers for the request.
            #               Ex.: yield scrapy.Request(url, headers={'User-Agent': 'my-custom-user-agent'})
            # 'cookies'  :  Allows you to send cookies with the request.
            #               Ex.: yield scrapy.Request(url, cookies={'sessionid': '12345'})
            #
            # 'handle_httpstatus_list' : 
            #               Allows handling specific HTTP status codes as part of normal 
            #               responses rather than errors. 
            #               Ex.: yield scrapy.Request(url, callback=self.parse_link, meta={'handle_httpstatus_list': [404, 500]}
            # ------------------------------------------------------------------------------------------
            yield scrapy.Request(url, callback=self.parse_link)

    # PREDEFINED METHOD
    # process_request: process each HTTP 'Request' from 'start_requests' before attempting to get a 'Response'
    def process_request(self, request, response):
        print('\nprocess_request', '1111111111111111111111111111111111111111111111111111111111111')
        # print(request.url, '\n', request.meta)   # request.meta.link_text
        request.meta['errback'] = self.parse_err_link   # what is meta 'errback' ? default recognized by scrapy ?
        print(request.url, '\n', request.meta, 'zzzzz\n')
        return request
    
    # PREDEFINED METHOD
    # parse: The default callback method for requests. If not otherwise specified, 
    #        Scrapy will use this method to handle responses. 
    #        Typically used to parse the initial response and extract data or additional URLs.
    # --------------------------------------------------------------------------------------------------
    def parse_link(self, response):
        parent_url = response.meta.get('parent_url', 'root')
        current_url = response.url

        print("\nparse_link 2222222222222222222222222222222222222222222222222222222222222")
        print(parent_url, current_url)
        # response.meta
        # {'rule': 0, 'link_text': 'Homepage, Link 3', 'depth': 1, 'download_timeout': 180.0, 'download_slot': 'localhost', 'download_latency': 0.00288}
        print(response.meta.get('zozo', 'link_text'),  'aaaa')
        print('\n\tHTTP: ', response.status, '\tURL: ', response.url, '\n')

        # Extract all links from the response
        links = response.css('a::attr(href)').getall()    # extract() vs. getall() ??
        for link in links:
            # Check if the URL is absolute or relative and create a proper URL
            full_url = response.urljoin(link)
            
            # Find the section containing references
            references_section = response.xpath("//h2[contains(., '7. References')]/following-sibling::ul")

            # Select all 'ul > li' items and extract their text
            list_items = response.css('ul > li::text').extract()
            # Select all 'ul > li' items and extract their text
            list_items = response.xpath('//ul/li/text()').extract()
            list_items = response.xpath('//ul/li')

            print('\nfull_url\n', full_url, '\nzzzzzzzzzzzzzzzzzaaaaaaaaaaaa\n', response.meta)
            # Check if the link is external (outside 'mysite.com')

            # To skip anchor links that direct to the same page
            # if href and not href.startswith('#'):
            
            if not link.startswith('http://localhost:700'):
                # Yield a dictionary with the external URL and status code
                yield {
                    'status': response.status,
                    response.url: full_url,
                }
                # ask chatGPT to save 'referer' and parent-child ; Crawled (for URLs) vs. Scraped (data requested)


    # PREDEFINED METHOD
    # 'errback' : Error handling method for requests. 
    #             If an error occurs during the processing of a request, 
    #             the errback method specified in the request's meta data will be called.
    # --------------------------------------------------------------------------------------------------
    # def errback(self, failure):
    #     pass

    def parse_err_link(self, failure):
        print("\nparse_error 3333333333333333333333333333333333333333333333333333333333333")
        print(failure.status, failure.url)
        pass


    # PREDEFINED METHOD
    # 'closed' : Called when the spider is closed. 
    #            This can be used to perform any cleanup or final processing. 
    #            The reason parameter indicates why the spider was closed.
    # --------------------------------------------------------------------------------------------------
    # def closed(self, reason):
    #     # Perform any cleanup or final processing here
    #     self.log(f"Spider closed because: {reason}")

