# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
class DoubanNovelSpider(scrapy.Spider):
    name = 'douban_novel'
    allowed_domains = ['douban.com']
    start_urls=['https://book.douban.com/tag/小说?start='+str(start)+'&type=T' for start in range(0,1000,20)]
    def parse(self,response):
        lis=response.xpath('//*[@id="subject_list"]/ul/li')
        for li in lis:
            item=DoubanItem()
            item["novel_writter"]=li.xpath('div[@class="info"]/div[@class="pub"]/text()').extract()[0].replace('\n','').strip().split('/')[0].strip()
            item["novel_pub"]=li.xpath('div[@class="info"]/div[@class="pub"]/text()').extract()[0].replace('\n','').strip().split('/')[-3].strip()
            item["novel_pub_date"]=li.xpath('div[@class="info"]/div[@class="pub"]/text()').extract()[0].replace('\n','').strip().split('/')[-2].strip()
            item["novel_price"]=li.xpath('div[@class="info"]/div[@class="pub"]/text()').extract()[0].replace('\n','').strip().split('/')[-1].strip().strip('元')
            item["novel_rating"]=li.xpath('div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract()[0]
            item["novel_rating_people_num"]=li.xpath('div[@class="info"]/div[@class="star clearfix"]/span[3]/text()').extract()[0].replace('\n','').strip().strip('(').strip(')').strip('人评价')
            item["novel_name"]=li.xpath('div[@class="info"]/h2/a/@title').extract()[0]
            yield item
