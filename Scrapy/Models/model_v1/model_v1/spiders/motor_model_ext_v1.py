import scrapy
import pandas as pd 
import numpy as np
from scrapy.crawler import CrawlerProcess

# class MotorBikeSpider(scrapy.Spider):
#     name = 'motor_model_ext_v1'
#     allowed_domains = ['https://www.ultimatespecs.com/motorcycles-specs']
#     start_urls = ['https://www.ultimatespecs.com/motorcycles-specs/']

#     def parse(self, response):  
#         brands = response.xpath('/html/body/section[1]/div/div/div/div/div')

#         brands01 = []
#         for brand in brands:
#             bikes = brand.xpath('.//div//h2//text()').extract()
#             bikes = str(bikes)
#             bikes = bikes.replace(" Specs","")
#             brands01.append(bikes)
#         brands02 = brands01[2]
#         brands02 = brands02.split(',')
#         # print(brands02)
        
        
#         # np.savetxt('bike_brands_v1.csv',brands01,delimiter=", ",fmt='% s')
#         # brands01 = np.array(brands01)
#         urls = []
#         for i in brands02:
#             # print(i)
#             item = str(i)
#             item = item.replace("['","")
#             item = item.replace("'","")
#             item = item.replace(" ","")
#             url = str('https://www.ultimatespecs.com/motorcycles-specs/'+item)
#             urls.append(url)
#         np.savetxt('bike_urls.csv',urls,delimiter=", ",fmt='% s')
#         print(urls)

class bike_model(scrapy.Spider):
    name = 'motor_model_ext_v1'
    # start_urls = [
    #     'https://www.ultimatespecs.com/motorcycles-specs/bajaj',
    #     'https://www.ultimatespecs.com/motorcycles-specs/Adiva',
    # ]
    with open('bike_urls.csv') as f:
        start_urls = f.readlines()
    # print(start_urls)

    def parse(self,response):
        for titles in response.xpath('//html/body/section[1]/div/div/div/div/div[3]/div[1]/div/div/div'):
            yield{
                'model':titles.xpath('.//a//text()').extract_first(),
            }

# process = CrawlerProcess()
# # process.crawl(MotorBikeSpider)
# process.crawl(bike_model)
# process.start()