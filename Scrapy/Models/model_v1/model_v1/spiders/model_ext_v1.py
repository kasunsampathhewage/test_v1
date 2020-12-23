import scrapy
import pandas as pd 
import numpy as np
from scrapy.crawler import CrawlerProcess

# class FinalSpider(scrapy.Spider):
#     name = 'model_ext_v1'
#     allowed_domains = ['https://www.ultimatespecs.com/car-specs']
#     start_urls = ['https://www.ultimatespecs.com/car-specs/']

#     def parse(self, response):  
#         brands = response.xpath('//html/body/section[1]/div/div[1]/div/div/div[3]/div[3]/div/div/div')
        

#         brands01 = []
#         for brand in brands:
#             cars = brand.xpath('.//a/@href').extract_first()
#             cars = str(cars)
#             brands01.append(cars)
#         # print(brands01)
#         # np.savetxt('brands_v1.csv',brands01,delimiter=", ",fmt='% s')

#         urls = []
#         for i in brands01:
#             url = str('https://www.ultimatespecs.com'+i)
#             urls.append(url)
#         np.savetxt('urls.csv',urls,delimiter=", ",fmt='% s')
#         # print(urls)

class car_model(scrapy.Spider):
    name = 'model_ext_v1'
    # start_urls = [
    #     'https://www.ultimatespecs.com/car-specs/Abarth-models',
    #     'https://www.ultimatespecs.com/car-specs/Toyota-models',
    # ]
    with open('urls.csv') as f:
        start_urls = f.readlines()

    def parse(self,response):
        for titles in response.xpath('//html/body/section[1]/div/div[1]/div/div/div[4]/div/div/div[4]/a/div/div'):
            yield{
                'model':titles.xpath('.//img/@alt').extract_first(),
            }

# process = CrawlerProcess()
# # process.crawl(FinalSpider)
# process.crawl(car_model)
# process.start()