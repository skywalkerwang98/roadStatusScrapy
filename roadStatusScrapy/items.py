# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RoadstatusscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    timeStamp = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
    direction = scrapy.Field()
    angle = scrapy.Field()
    speed = scrapy.Field()
    lcodes = scrapy.Field()
    polyline = scrapy.Field()