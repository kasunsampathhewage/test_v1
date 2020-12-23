import scrapy
import numpy as np


class ModelsSpider(scrapy.Spider):
    name = 'models'
    allowed_domains = ['https://www.ultimatespecs.com/car-specs/Toyota-models']
    start_urls = ['https://www.ultimatespecs.com/car-specs/Toyota-models/']

    def parse(self, response):
        all_models = response.xpath('//div[2]')

        models = []
        for models in all_models:
            title = models.xpath('.//img/@alt').extract_first()
            # title = str(title)
            print(title)
            # models.append(title)
        # print(models)
        # np.savetxt('models1.csv',models,delimiter=", ",fmt='% s')
        # yield title


