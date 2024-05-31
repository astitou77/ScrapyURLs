import scrapy


class IetfSpider(scrapy.Spider):
    name = "ietf"
    allowed_domains = ["canada.ca"]
    start_urls = ["https://www.canada.ca/en/department-national-defence/corporate/policies-standards/defence-administrative-orders-directives.html"]

    def parse(self, response):
        # rfc = response.xpath('//span[@class="rfc-no"]//get()')
        # title = response.css("span.title::text").get()
        description = response.xpath('//div[@class="row wb-eqht-grd"]//h3//a/text()').getall()

        yield {'description': description}
