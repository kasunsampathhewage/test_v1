import scrapy
import numpy as np



class Models03Spider(scrapy.Spider):
    name = 'models03'
    allowed_domains = ['https://www.ultimatespecs.com/car-specs/Toyota-models/']
    start_urls = ['https://www.ultimatespecs.com/car-specs/Toyota-models//']

    def parse(self, response):
        all_models = response.xpath('//html/body/section[1]/div/div[1]/div/div/div[4]/div/div/div[4]/a/div/div')

        models01 = []
        for models in all_models:
            title = models.xpath('.//img/@alt').extract_first()
            title = str(title)
            models01.append(title)
        print(models01)
        np.savetxt('models1.csv',models01,delimiter=", ",fmt='% s')

# /html/body/section[1]/div/div[1]/div/div/div[4]/div/div/div[4]/a/div/div/img/@class

