import scrapy
import pandas as pd 
import numpy as np
from scrapy.crawler import CrawlerProcess

# class TractorSpider(scrapy.Spider):
#     name = 'tractor_model_ext_v1'
#     allowed_domains = ['https://www.ultimatespecs.com/tractor-specs/']
#     start_urls = ['https://www.ultimatespecs.com/tractor-specs/']

#     def parse(self, response):  
#         brands = response.xpath('/html/body/section[1]/div/div/div/div/div[3]/div[2]/div/a/div/div')

#         brands01 = []
#         for brand in brands:
#             tractors = brand.xpath('.//div//h2//text()').extract()
#             tractors = str(tractors)
#             tractors = tractors.replace(" Specs","")
#             brands01.append(tractors)
#         # print(brands01)
        
        
# #         # np.savetxt('bike_brands_v1.csv',brands01,delimiter=", ",fmt='% s')
# #         # brands01 = np.array(brands01)
#         urls = []
#         for i in brands01:
#             # print(i)
#             item = str(i)
#             item = item.replace("['","")
#             item = item.replace("'","")
#             item = item.replace(" ","")
#             item = item.replace("]","")
#             url = str('https://www.ultimatespecs.com/tractor-specs/'+item)
#             urls.append(url)
#         np.savetxt('tractor_urls.csv',urls,delimiter=", ",fmt='% s')
#         # print(urls)

class tractor_model(scrapy.Spider):
    name = 'tractor_model_ext_v1'
    # start_urls = [
    #     'https://www.ultimatespecs.com/motorcycles-specs/bajaj',
    #     'https://www.ultimatespecs.com/motorcycles-specs/Adiva',
    # ]
    with open('tractor_urls.csv') as f:
        start_urls = f.readlines()
    # print(start_urls)

    def parse(self,response):
        for titles in response.xpath('//html/body/section[1]/div/div/div/div/div[3]/div[1]/div/div/div'):
            yield{
                'model':titles.xpath('.//a//text()').extract_first(),
            }




# process = CrawlerProcess()
# # process.crawl(TractorSpider)
# process.crawl(tractor_model)
# process.start()