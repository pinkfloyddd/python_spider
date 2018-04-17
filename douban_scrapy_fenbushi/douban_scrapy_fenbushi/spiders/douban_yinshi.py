# -*- coding: utf-8 -*-

import scrapy
from douban_scrapy_fenbushi.items import DoubanScrapyFenbushiItem
import json
import requests
class DoubanYinshiSpider(scrapy.Spider):
    name = 'douban_yinshi'
    allowed_domains = ['douban.com']
    def start_requests(self):
        start = 0
        while True:
            urls = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=' + str(start)
            j1 = json.loads(requests.get(urls).text)
            l1s = j1['data']
            if l1s is None:
                break
            else:
                for l1 in l1s:
                    href=l1['url']
                    print(href)
                    yield scrapy.Request(href)
                    start += 10
    def parse(self, response):
        item = DoubanScrapyFenbushiItem()
        item["name"] = response.xpath('//*[@id="content"]/h1/span[1]/text()').extract()[0]
        item["date"] = response.xpath('//*[@id="content"]/h1/span[2]/text()').extract()[0].strip('(').strip(')')
        item["type"] = response.xpath('//div[@id="info"]/span[@property="v:genre"]/text()').extract()[0]
        item["country"] = response.xpath('//span[text()="制片国家/地区:"]/following::text()[1]').extract()[0].strip()
        item["langue"] = response.xpath('//span[text()="语言:"]/following::text()[1]').extract()[0].strip()
        item["rating"] = response.xpath('//strong[@class="ll rating_num"]/text()').extract()[0]
        item["rating_nums"] = response.xpath('//div[@class="rating_sum"]/a/span[1]/text()').extract()[0]
        yield item