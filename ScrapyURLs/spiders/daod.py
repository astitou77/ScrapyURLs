import scrapy

class DAOD(scrapy.Spider):
    name = "daod"
    # allowed_domains = ["www.canada.ca"]
    start_urls = ["https://www.canada.ca/en/department-national-defence/corporate/policies-standards/defence-administrative-orders-directives/1000-series/1000/1000-0-foundation-framework-defence-administrative-orders-directives.html"]


    def parse(self, response):
        # Extract all <a> elements from the response
        links = response.css('div.mwsbodytext ul li a')

        for link in links:
            # Extract the href attribute and text content
            href = link.css('::attr(href)').get()
            text = link.css('::text').get()
            
            if href and not href.startswith('#'):
                # Construct the full URL
                full_url = response.urljoin(href)

                # Yield a request to check the status of the link, with dont_filter=True to keep duplicates
                yield scrapy.Request(
                    full_url, 
                    callback=self.parse_link, 
                    errback=self.handle_error, 
                    meta={'text': text, 'full_url': full_url}, 
                    dont_filter=True
                )

    def parse_link(self, response):
        # Extract the URL and status code from the response
        status = response.status
        text = response.meta['text']
        full_url = response.meta['full_url']

        # Yield a dictionary with URL, status, and link text
        if not (200 <= status < 300):
            yield {
                'http': status,
                text: full_url
            }

    def handle_error(self, failure):
        # Handle HTTP errors such as 404
        response = failure.value.response
        status = response.status
        text = response.meta['text']
        full_url = response.meta['full_url']

        # Yield a dictionary with URL, status, and link text
        yield {
            'http': status,
            text: full_url
        }

