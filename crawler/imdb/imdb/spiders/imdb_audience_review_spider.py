#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from imdb.items import AudienceReviewItem as ReviewItem
from imdb.items import MovieItem
from scrapy.contrib.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor


class AudienceReviewItem(CrawlSpider):
    """Documentation for AudienceReviewItem

    """
    name = 'audience_review'
    allowed_domain = ['imdb.com']
    start_urls = [
        'http://www.imdb.com/title/tt0111161/reviews?ref_=tt_urv'
    ]
    audience_Extractor = LinkExtractor(
        allow=(r'reviews\?start=.*')
    )
    rules = (
        Rule(audience_Extractor, callback='parse_audience_review'),
    )

    def parse_audience_review(self, response):
        title = response.xpath(
            "//div[@id='tn15content']/div/h2/text()").extract()
        author = response.xpath(
            "//div[@id='tn15content']/div/a[2]/text()").extract()
        time = response.xpath(
            "//div[@id='tn15content']/div/small[3]/text()").extract()
        content = response.xpath("//div[@id='tn15content']/p").extract()
        usage = response.xpath(
            "//div[@id='tn15content']/div/small[1]/text()").extract()
        result = zip(title, author, time, content, usage)
        for title_item, author_item, time_item, content_item, usage_item in result:
            item = ReviewItem()
            item['title'] = title_item
            item['author'] = author_item
            item['time'] = time_item
            item['content'] = content_item
            item['usage'] = usage_item
            yield item
