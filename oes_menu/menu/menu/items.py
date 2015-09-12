# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MenuItem(scrapy.Item):
    menu = scrapy.Field()
    days = scrapy.Field()
    date = scrapy.Field()
