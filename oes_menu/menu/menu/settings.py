# -*- coding: utf-8 -*-

# Scrapy settings for menu project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'menu'
FEED_FORMAT = 'json'

SPIDER_MODULES = ['menu.spiders']
NEWSPIDER_MODULE = 'menu.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'menu (+http://www.yourdomain.com)'
