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
            'classic': 4,
            'global': 5,
            'dinner': 6,
            'dessert': 3,
        }

        def cell_selector(day, meal):
            return (
                'tbody tr:nth-child(' + str(meal) + ') '
                'td:nth-child(' + str(day+2) + ') '
            )

        def css_extract(selector, default=''):
            return response.css(selector).extract_first(default=default)

        def menu_item(day, meal):
            menu_item_sel = 'strong:first-child span::text'
            return css_extract(cell_selector(day, meal) + menu_item_sel)

        def description(day, meal):
            desc_sel = '.menu-item-description:first-child .collapsed::text'
            selector = cell_selector(day, meal) + desc_sel
            description = css_extract(selector)
            if len(description):
                return "<div class='item-desc'>" + css_extract(selector) + "</div>"
            else:
                return  description

        def date_for_day(day):
            selector = 'thead td:nth-child(' + str(day+2) + ')::text'
            full_heading = css_extract(selector)
            # Remove weekday from date string
            return re.sub(r'^.*-\s', '', str(full_heading)).strip()

        for day in range(5): # For 5 Days of Week
            item['days'].append({})
            for meal_name, meal_row in meal_row_map.iteritems():
                meal = item['days'][day][meal_name] = {}
                meal['title'] = menu_item(day, meal_row)
                meal['desc'] = description(day, meal_row)


        item['date'] = date_for_day(1) + ' - ' + date_for_day(5)
        return item
