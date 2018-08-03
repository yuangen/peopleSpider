# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PeoplespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_title = scrapy.Field()
    news_author = scrapy.Field()
    news_time = scrapy.Field()
    news_content = scrapy.Field()
    news_comment = scrapy.Field()
    news_source = scrapy.Field()
