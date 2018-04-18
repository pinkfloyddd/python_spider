# -*- coding: utf-8 -*-
import scrapy


class DoubanCeshiSpider(scrapy.Spider):
    name = 'douban_ceshi'
    allowed_domains = ['douban.com']
    start_urls=['https://book.douban.com/tag/小说?start='+str(start)+'&type=T' for start in range(0,1020,20)]
    def parse(self, response):
        lis=response.xpath('//*[@id="subject_list"]/ul/li')
        lis_list=list(lis)
#        print(type(lis))
#        print(type(lis_list))
        print(len(lis_list))
