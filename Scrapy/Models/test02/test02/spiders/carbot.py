# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess

class CarbotSpider(scrapy.Spider):
    name = 'carbot'
    allowed_domains = ['ultimatespecs.com']
    start_urls = ['https://www.ultimatespecs.com/car-specs']

    def parse(self, response):
        manufacturers = response.xpath('//div[@class="table_makes"]/div/div/a/@href').extract()
        for manufacture in manufacturers:
            url = 'https://www.ultimatespecs.com'+str(manufacture)
            yield scrapy.Request(url=url,callback=self.parse_manufacturer)

    def parse_manufacturer(self, response):
        models = response.xpath('//div[@class="home_models_line"]/a/@href').extract()
        for model in models:
            url = 'https://www.ultimatespecs.com'+str(model)
            yield scrapy.Request(url=url,callback=self.parse_model)

    def parse_model(self, response):
        url = response.url
        manufacturer_name = response.xpath('//div[@class="breadcrumb"]//a/text()').extract()[1]
        model_name = url.split('/')[-1].replace('-',' ')

        print('\x1b[1;35;40m' + url + '\x1b[0m')
        print('\x1b[1;34;40m' + str(manufacturer_name) + '\x1b[0m')
        print('\x1b[1;34;40m' + str(model_name) + '\x1b[0m')

        yield {
                'manufacturer' : str(manufacturer_name),
                'model' : str(model_name)
        }


process = CrawlerProcess()
# # process.crawl(FinalSpider)
process.crawl(CarbotSpider)
process.start()