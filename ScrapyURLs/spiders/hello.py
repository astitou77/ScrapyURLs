import scrapy


class HelloSpider(scrapy.Spider):
    name = "hello"
    allowed_domains = ["www.localhost"]
    start_urls = ["http://localhost:700"]

    def parse(self, response):
        links = response.css("div ul li a")

        for link in links:
            href = link.css('::attr(href)').get()

            if href:
                url = response.urljoin(href)

                yield {
                    'url': url 
                }
