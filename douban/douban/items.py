# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    novel_name=scrapy.Field()
    novel_writter=scrapy.Field()
    novel_rating=scrapy.Field()
    novel_price=scrapy.Field()
    novel_rating_people_num=scrapy.Field()
    novel_pub=scrapy.Field()
    novel_pub_date=scrapy.Field()
