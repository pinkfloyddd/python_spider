# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymsql
from pymysql import connection
from douban_scrapy_fenbushi.items import DoubanScrapyFenbushiItem

class DoubanScrapyFenbushiPipeline(object):
    def __init__(self):
        self.dbcon = pymsql.connect(host='192.168.138.132',user='douban_admin',passwd='zhaoye861227',
                                    db='douban',use_unicode=True,charset='utf8')
        self.coursor = self.dbcon.cursor()
    def process_item(self, item, spider):
        name = item["name"]
        type = item["type"]
        date = item["date"]
        country = item["country"]
        langue = item["langue"]
        rating = item["rating"]
        rating_nums = item["rating_nums"]
        sql = "insert into douban_yinshi(name,type,country,date,langue,rating,rating_nums) value(%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.coursor.execute(sql,(name,type,country,date,langue,rating,rating_nums))
            self.dbcon.commit()
        except:
            print("数据库插入失败")
            self.dbcon.rollback()
        else:
            print("数据库插入成功")
        self.dbcon.close()
        return item


