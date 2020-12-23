import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['https://auto-types.com/cars-specifications']
    start_urls = ['https://auto-types.com/cars-specifications/']

    def parse(self, response):
        # titles = response.css(".titleNews").extract()
        titles = response.xpath('//div')

        for car in titles:
            # scraped_info={'title':item[0]}
            title = car.xpath('.//a/@title').extract()
            # print(title)

            yield title

        