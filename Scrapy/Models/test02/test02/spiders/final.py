import scrapy
import numpy as np
from scrapy.crawler import CrawlerProcess
import pandas as pd
from numpy import genfromtxt



# class FinalSpider(scrapy.Spider):
#     name = 'final'
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

# url = pd.read_csv('urls.csv')
# url = pd.DataFrame(url)
# url01 = url.values.tolist()


class Cars01Spider(scrapy.Spider):
    name = 'final'
    # allowed_domains = ['https://www.ultimatespecs.com/car-specs/']
    # start_urls = [l.strip() for l in open('urls_v1.csv').readlines()]
    urls1 = pd.read_csv('urls_v1.csv')
    urls1 = pd.DataFrame(urls1)
    urls = []
    for ur in urls1:
        urls.append(ur)
    start_urls = ['https://www.ultimatespecs.com/car-specs/Abarth-models',
                    'https://www.ultimatespecs.com/car-specs/Toyota-models',]


    # def start_requests(self):
    #     # urls = [l.strip() for l in open('urls_v1.csv').readlines()]

    #     urls1 = pd.read_csv('urls_v1.csv')
    #     urls1 = pd.DataFrame(urls1)

    #     urls = []
    #     for ur in urls1:
    #         urls.append(ur)
    #     # print(urls)
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        models01 = []
        all_models = response.xpath('//html/body/section[1]/div/div[1]/div/div/div[4]/div/div/div[4]/a/div/div/img/@alt').extract()
        # print(all_models)  

                                  
        
        for titles in all_models:
            # title = models.xpath('.//img/@alt').extract_first()
            title = str(titles)
            # print(title)
            models01.append(title)
            # print(title)
        # print(models01)
        # yield{models01}
        # np.savetxt('models_v1.csv',models01,delimiter=", ",fmt='% s')
        

    
                

# process = CrawlerProcess()
# # # process.crawl(FinalSpider)
# process.crawl(Cars01Spider)
# process.start()