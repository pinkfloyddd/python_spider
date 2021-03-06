# -*- coding: utf-8 -*-

import scrapy
from douban_scrapy_fenbushi.items import DoubanScrapyFenbushiItem
import json
import requests
from PIL import Image
from scrapy.http import FormRequest
import fake_useragent

class DoubanYinshiSpider(scrapy.Spider):
    name = 'douban_yinshi'
    allowed_domains = ['douban.com']
    ua = fake_useragent.UserAgent()
    UserAgent = ua.random
    header = {'User-Agent':UserAgent}
    def start_requests(self):
        urls = 'https://accounts.douban.com/login'
        return [scrapy.Request(url=urls,callback=self.login_parse,meta={'cookiejar':1},headers=self.header)]
    def login_parse(self, response):
        print('开始登陆')
        captcha_url = response.xpath('//img[@id="captcha_image"]/@src').extract()
        if captcha_url != []:
            print('有验证码登陆')
            captcha_get = requests.get(captcha_url[0])
            with open('captcha.jpg', 'wb') as fp:
                fp.write(captcha_get.content)
                fp.close()
            captcha_img = Image.open('captcha.jpg')
            captcha_img.show()
            captcha_vale = input('请输入验证码：')
            captcha_img.close()
            data = {'form_email': '15026435190', 'form_password': 'zhaoye861227', 'redir': 'https://douban.com','captcha-solution': captcha_vale}
        else:
            print('无验证码登陆')
            data = {'form_email': '15026435190', 'form_password': 'zhaoye861227', 'redir': 'https://douban.com'}
        return FormRequest.from_response(response, meta={'cookiejar': response.meta["cookiejar"]}, formdata=data,callback=self.after_login,headers=self.header)
    def after_login(self,response):
        title = response.xpath('//title/text()').extract()[0]
        if '登录豆瓣' in title:
            print('登录失败')
        else:
            print('登录成功 ')
            print('开始爬取')
            # print(response.headers.getlist("Set-Cookie"))
            # print(response.request.headers)
            start = 0
            while True:
                urls = ['https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=' + str(start)]
                for url in urls:
                    j1 = json.loads(requests.get(url).text)
                    l1s = j1["data"]
                    if l1s is None:
                        break
                    else:
                        for l1 in l1s:
                            href=l1["url"]
                            yield scrapy.Request(url=href,meta={'cookiejar':True},callback=self.detail_parse,headers=self.header)
                            start += 1
    def detail_parse(self, response):
        item = DoubanScrapyFenbushiItem()
        item["name"] = response.xpath('//*[@id="content"]/h1/span[1]/text()').extract()[0]
        item["date"] = response.xpath('//*[@id="content"]/h1/span[2]/text()').extract()[0].strip('(').strip(')')
        item["type"] = response.xpath('//div[@id="info"]/span[@property="v:genre"]/text()').extract()[0]
        item["country"] = response.xpath('//span[text()="制片国家/地区:"]/following::text()[1]').extract()[0].strip()
        item["langue"] = response.xpath('//span[text()="语言:"]/following::text()[1]').extract()[0].strip()
        item["rating"] = response.xpath('//strong[@class="ll rating_num"]/text()').extract()[0]
        item["rating_nums"] = response.xpath('//div[@class="rating_sum"]/a/span[1]/text()').extract()[0]
        yield item