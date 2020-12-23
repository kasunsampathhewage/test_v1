import scrapy
import pandas as pd 
import numpy as np
from scrapy.crawler import CrawlerProcess

class IndianBusesSpider(scrapy.Spider):
    name = 'indian_buses_ext'
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    start_urls = ['https://buses.cardekho.com/filter/bus.html',]

    def parse(self,response):
        for titles in response.xpath('//html/body/section/div/div[3]/div[2]'):
            yield{
                'model':titles.xpath('.//ul').extract(),
                # 'price':titles.xpath('.//div/text()').extract(),
            }

process = CrawlerProcess()
# process.crawl(TractorSpider)
process.crawl(IndianBusesSpider)
process.start()

# /html/body/div[4]/div[1]/div[1]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div/section/div/div/div/div/div/text()
# /html/body/div[4]/div[1]/div[1]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div/section/div/div/div/div
# /html/body/div[4]/div[1]/div[1]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div//div/div/div/div/div[2]/text()