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
        item['days'] = []

        meal_row_map = {
            'classic': 3,
            'global': 4,
            'dinner': 5,
        }

        def strip_tags_from(markup):
            return str(re.sub(r'<[^<]+?>', '', markup.encode('utf-8')))

        def css_query(day, meal):
            css_query = (
                'tbody tr:nth-child(' + str(meal) + ') '
                'td:nth-child(' + str(day+2) + ') '
                'strong:nth-child(1) span'
            )
            return strip_tags_from(response.css(css_query).extract()[0])

        for day in range(5): # For 5 Days of Week
            item['days'].append({})
            for meal_name, meal_row in meal_row_map.iteritems():
                try:
                    item['days'][day][meal_name] = css_query(day, meal_row)
                except IndexError:
                    print "NO VALUE"

        def date_for_day(day):
            css_query = 'thead td:nth-child(' + str(day+2) + ')'
            full_heading = strip_tags_from(response.css(css_query).extract()[0])
            return re.sub(r'^.*-\s', '', str(full_heading)).strip()

        item['date'] = date_for_day(1) + ' - ' + date_for_day(5)
        return item
