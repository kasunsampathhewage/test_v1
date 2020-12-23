import scrapy
import pandas as pd 
import numpy as np
from scrapy.crawler import CrawlerProcess

class TruckSpider(scrapy.Spider):
    name = 'truck_model_ext_v1'

    # start_urls = [
    #     'https://carused.jp/car-list?category_id=35',
    #     'https://carused.jp/car-list?category_id=35&page=2',
    # ]
    start_urls = [
        'https://carused.jp/car-list?category_id=35&page=1',
    ]

    def parse(self,response):
        next_page = response.xpath('//html/body/div[5]/main/nav/ul/li/a//text()').extract()
        next_page = next_page[:-1]
        page = []
        for pages in next_page:
            pages = 'https://carused.jp/car-list?category_id=35&page='+pages
            page.append(str(pages))
        # print(page)
        np.savetxt('truck_urls.csv',page,delimiter=", ",fmt='% s')

class TruckModelSpider(scrapy.Spider):
    name = 'truck_model_ext_v2'

    with open('truck_urls.csv') as f:
        start_urls = f.readlines()

    def parse(self,response):
        for titles in response.xpath('//html/body/div/main/section[6]/div[3]/ul/li/div/a/ul'):
            yield{
                'model':titles.xpath('.//li/h2//text()').extract_first(),
                'year' :titles.xpath('.//li[3]//text()').extract_first(),
                'milage' :titles.xpath('.//li[4]//text()').extract_first(),
                'engine' :titles.xpath('.//li[5]//text()').extract_first(),
                'transmission' :titles.xpath('.//li[6]//text()').extract_first(),
                'drive' :titles.xpath('.//li[7]//text()').extract_first(),
                'steer' :titles.xpath('.//li[8]//text()').extract_first(),
                'price' :titles.xpath('.//li[9]/b//text()').extract_first(),
            }
            
        models = pd.read_csv('truck_models.csv')
        df = pd.DataFrame(models)
        df[['brand', 'model_type']] = df['model'].str.split(' ', 1, expand=True)
        df = df[['brand', 'model']]    


