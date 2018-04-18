# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from pymysql import connections
from douban.items import DoubanItem
class DoubanPipeline(object):
    def __init__(self):
        self.dbcon=pymysql.connect(host='192.168.138.132',user='douban_admin',passwd='zhaoye861227',db='douban',use_unicode=True,charset='utf8')
        self.coursor=self.dbcon.cursor()
    def process_item(self, item, spider):
        name=item["novel_name"]
        writter=item["novel_writter"]
        pub=item["novel_pub"]
        pub_date=item["novel_pub_date"]
        price=item["novel_price"]
        rating=item["novel_rating"]
        rating_nums=item["novel_rating_people_num"]
        sql="insert into douban_tushu_xiaoshuo(name,writter,pub,pub_date,price,rating,rating_nums) value(%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.coursor.execute(sql,(name,writter,pub,pub_date,price,rating,rating_nums))
            self.dbcon.commit()
        except:
            print("数据库插入失败")
            self.dbcon.rollback()
        else:
            print('数据库插入成功')
        return item
        self.dbcon.close()
