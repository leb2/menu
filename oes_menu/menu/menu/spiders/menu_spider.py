# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import *
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule


class MenuSpiderSpider(CrawlSpider):
    name = "menu_spider"
    allowed_domains = ["oes.cafebonappetit.com", "legacy.cafebonappetit.com"]
    start_urls = ['http://oes.cafebonappetit.com']
    rules = [Rule(LinkExtractor(allow=['.*/weekly-menu/\d+']), "parse_menu")]

    def parse_menu(self, response):
        item = MenuItem()
        # item['menu'] = response.css('table').extract()
        # day = item['days'][i]
        item['days'] = []

        def css_query(day, meal):
            return 'tbody tr:nth-child(' + str(meal) + ') td:nth-child(' + str(i+2) + ') strong:nth-child(1) span'

        for i in range(5): # For 5 Days of Week
            item['days'].append({})
            item['days'][i]['classic'] = str(re.sub('<[^<]+?>', '', str(response.css(css_query(i, 5)).extract()[0])))
            print item['days'][i]['classic']
            item['days'][i]['global'] = str(re.sub('<[^<]+?>', '', str(response.css(css_query(i, 6)).extract()[0])))
            item['days'][i]['dinner'] = str(re.sub('<[^<]+?>', '', str(response.css(css_query(i, 7)).extract()[0])))

            # Dessert only on odd days
            item['days'][i]['dessert'] = ''
            if i % 2 == 0:
                item['days'][i]['dessert'] = str(re.sub('<[^<]+?>', '', str(response.css(css_query(i, 3)).extract()[0])))

        return item
