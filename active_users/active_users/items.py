# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ActiveUserItem(scrapy.Item):
    uid = scrapy.Field()
    nname = scrapy.Field()  # Normalized name
