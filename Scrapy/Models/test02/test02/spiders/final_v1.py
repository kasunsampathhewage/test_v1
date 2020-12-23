import scrapy
import numpy as np
from scrapy.crawler import CrawlerProcess
import pandas as pd
from numpy import genfromtxt



class Cars02Spider(scrapy.Spider):
    name = 'final_v1'
    # allowed_domains = ['https://www.ultimatespecs.com/car-specs/']
    # start_urls = [l.strip() for l in open('urls_v1.csv').readlines()]
    # urls1 = pd.read_csv('urls_v1.csv')
    # urls1 = pd.DataFrame(urls1)
    # urls = []
    # for ur in urls1:
    #     urls.append(ur)
    start_urls = ['https://www.ultimatespecs.com/car-specs/Abarth-models',
                    'https://www.ultimatespecs.com/car-specs/Toyota-models',]


    def parse(self,response):
       all_models = response.xpath('//html/body/section[1]/div/div[1]/div/div/div[4]/div/div/div[4]/a/div/div/img/@alt').extract()

       for items in all_models:
           yield{'model':items}
    
                

# process = CrawlerProcess()
# # # process.crawl(FinalSpider)
# process.crawl(Cars02Spider)
# process.start()