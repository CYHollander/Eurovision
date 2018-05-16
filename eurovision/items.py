# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class country(scrapy.Item):
    song = scrapy.Field()
    title = scrapy.Field()
    singer = scrapy.Field()
    conductor = scrapy.Field()
    language = scrapy.Field()
    votes_received = scrapy.Field()
    place = scrapy.Field()