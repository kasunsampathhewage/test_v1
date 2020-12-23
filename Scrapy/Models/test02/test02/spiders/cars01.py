import scrapy
import numpy as np


class Cars01Spider(scrapy.Spider):
    name = 'cars01'
    allowed_domains = ['https://www.ultimatespecs.com/car-specs']
    start_urls = ['https://www.ultimatespecs.com/car-specs/']

    def parse(self, response):
        brands = response.xpath('//html/body/section[1]/div/div[1]/div/div/div[3]/div[3]/div/div/div')
        # brands = response.xpath('//[@id="car_make"]/div[3]/div/div[1]/a')

        brands01 = []
        for brand in brands:
            cars = brand.xpath('.//a/@href').extract_first()
            cars = str(cars)
            brands01.append(cars)
        print(brands01)
        np.savetxt('brands.csv',brands01,delimiter=", ",fmt='% s')
            # yield cars


# /html/body/section[1]/div/div[1]/div/div/div[3]/div[3]/div/div/div/a