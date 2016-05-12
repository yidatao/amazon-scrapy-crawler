# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class PostprocessPipeline(object):

    def process_item(self, item, spider):
        if 'brand' not in item:
            raise DropItem("No brand in %s" % item)

        r = item['rating']
        if len(r) > 0:
            rating = r[0]
            item['rating'] = float(rating[:rating.index(' ')])
        else:
            raise DropItem("No rating in %s" % item)

        if len(item['price']) > 0:
            item['price'] = item['price'][0][1:]
        else:
            raise DropItem("No price in %s" % item)

        if len(item['name']) > 0:
            item['name'] = item['name'][0]
        if len(item['reviews']) > 0:
            review = item['reviews'][0]
            item['reviews'] = review[:review.index(' ')]
        if len(item['save']) > 0:
            save = item['save'][0]
            item['save'] = save[1:save.index('(')].strip()
            item['savePercent'] = save[save.index('(')+1:save.index('%')]
        else:
            item['save'] = '0'
            item['savePercent'] = '0'
        if len(item['display']) > 0:
            item['display'] = item['display'][0]
        if len(item['size']) > 0:
            size = item['size'][0]
            index = size.find(' ')
            if index != -1:
                item['size'] = size[:index]
            else:
                item['size'] = size
        return item

# Using Twisted adbapi for non-blocking database access
from twisted.enterprise import adbapi
class MariaDBPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = dict(host=crawler.settings.get('DB_HOST'),
                      db=crawler.settings.get('DB'),
                      user=crawler.settings.get('DB_USER'))
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        try:
            sql = 'insert into TV values (%s,%s,%s,%s,%s,%s,%s,%s)'
            values = (item['brand'],item['name'],item['url'],item['rating'],item['reviews'],item['price'],item['save'],item['savePercent'])
            self.dbpool.runQuery(sql, values)
        except Exception as e:
            print(item)
            print(e)