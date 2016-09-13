# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    year = scrapy.Field()
    rate = scrapy.Field()
    director = scrapy.Field()
    storyline = scrapy.Field()
    audience_review = scrapy.Field()


class AudienceReviewItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    usage = scrapy.Field()
