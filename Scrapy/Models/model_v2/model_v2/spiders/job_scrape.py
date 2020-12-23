import scrapy
import pandas as pd 
import numpy as np
# from scrapy.crawler import CrawlerProcess


# class JobURLSpider(scrapy.Spider):
#     name = "job_scrape"

#     start_urls = ['https://www.topjobs.lk/index.jsp',]

#     def parse (self,response):
#         urls = response.xpath ('//html/body/div[4]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div')
#         # print(urls)
#         links = []
#         for url in urls:
#             url = urls.xpath('.//a/@href').extract()
#             links.append(url)
            
#         links = links[0]

#         urls = []
#         for i in links:
#             item = str(i)
#             url = ('https://www.topjobs.lk/')+item
#             urls.append(url)
#             # print(url)
#         urls = urls[:-1]
#         print(urls)
#         np.savetxt('job_urls.csv',urls,delimiter=", ",fmt='% s')

    # def parse(self,response):
    #     for titles in response.xpath('//html/body/div[4]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div'):
    #      yield{
    #          'name':titles.xpath('.//a//text()').extract_first(),
    #          'links':titles.xpath('.//a/@href').extract_first(),
    #      }

class JobURLSpiderModel(scrapy.Spider):
    name = 'job_scrape'
    # start_urls = [
    #     'https://www.topjobs.lk/applicant/vacancybyfunctionalarea.jsp;jsessionid=A-eLz1525tqjJYPqHmie7jc5?FA=BAF',
        
    # ]
    with open('job_urls.csv') as f:
        start_urls = f.readlines()
        print(start_urls)

    def parse(self,response):
        for titles in response.xpath('//*[@id="table"]/tr'):
            yield{
                'company':titles.xpath('.//h1//text()').extract(),
                'job':titles.xpath('.//h2//text()').extract(),
                'link':titles.xpath('.//h2/a/@href').extract(),
                'experience':titles.xpath('.//td[4]//text()').extract(),
                'opening_date':titles.xpath('.//td[5]//text()').extract(),
                'closing_date':titles.xpath('.//td[7]//text()').extract(),
            }
        
        # print(yield)

# /html/body/div[9]/div/table/tbody/tr[1]/td[3]/h2/a
# process = CrawlerProcess()
# # process.crawl(JobURLSpider)
# process.crawl(JobURLSpiderModel)
# process.start()