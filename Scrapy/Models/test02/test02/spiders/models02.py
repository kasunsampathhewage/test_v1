import scrapy
import numpy as np


class Models02Spider(scrapy.Spider):
    name = 'models02'
    allowed_domains = ['https://www.ultimatespecs.com/car-specs/Toyota-models/Toyota-Yaris']
    start_urls = ['https://www.ultimatespecs.com/car-specs/Toyota-models/Toyota-Yaris/']

    
    def parse(self, response):
        all_models02 = response.xpath('//div[2]')

        titles = []
        for models02 in all_models02:
            models = models02.xpath('.//img/@alt').extract_first()  
            models = str(models)
            titles.append(models)
            # print(models)
        yield titles
        print(titles)
        np.savetxt('sub_models.csv',titles,delimiter=", ",fmt='% s')
   
