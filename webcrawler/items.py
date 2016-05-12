# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    price = scrapy.Field()
    save = scrapy.Field()
    savePercent = scrapy.Field()
    display = scrapy.Field()
    size = scrapy.Field()
