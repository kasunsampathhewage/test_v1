import scrapy

class TestSpider(scrapy.Spider):
    name = 'test02'
    allowed_domains = ['https://auto-types.com/cars/abarth']
    start_urls = ['https://auto-types.com/cars/abarth']

    def parse(self, response):
        details = response.xpath('//div[3]')

        for models in details:
            model = models.xpath('.//div[@class="model-title"]/text()').extract()
            # model = models.xpath('.//div/@class').extract()
            print(model[0])
            # yield model

# //*[@id="content"]/div[2]/div[2]/div[1]

# //*[@id="content"]/div[3]/div[2]


        