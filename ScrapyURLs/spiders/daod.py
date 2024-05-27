import scrapy

class DAOD(scrapy.Spider):
    name = "daod"
    allowed_domains = ["www.canada.ca"]
    start_urls = ["https://www.canada.ca/en/department-national-defence/corporate/policies-standards/defence-administrative-orders-directives/1000-series/1000/1000-0-foundation-framework-defence-administrative-orders-directives.html"]

    def parse(self, response):
        # '<a href="#"> some text content </a>'
        for a in response.css('div.mwsbodytext ul li a'):
            # 'some text content'
            text = a.css('::text').get()
            # ignore same page anchor links | href='#'
            if a.attrib['href'][0] != "#":
                full_url = a.attrib['href']
                if a.attrib['href'][0] == "/":
                    full_url = response.urljoin(a.attrib['href'])
                    # NEXT: get status of each url
                yield{
                    'status': '200', #'scrapy.Request(url, callback=self.parse_link)',
                    text: full_url 
                }
    
    # def parse_link(self, response):
    #     status = response.status
    #     yield{
    #         'status': status
    #     }

