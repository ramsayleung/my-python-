#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from imdb.items import MovieItem
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from urlparse import urljoin


class ImdbSpider(CrawlSpider):
    """Documentation for ImdbSpider

    """
    audience_review_url = []
    name = 'imdb'
    allowed_domain = ['imdb.com']
    start_urls = [
        'http://www.imdb.com/chart/top/?ref_=nv_mv_250_6'
    ]
    movie_Extractor = LxmlLinkExtractor(allow=(
        r'/title/tt\d+/\?pf_rd_m=[\w?=]+'),
        tags=('a', 'title'), attrs=('href'), unique=True)
    audience_Extractor = LxmlLinkExtractor(
        allow=(r'http://www.imdb.com/title/tt\d+/reviews?ref_=tt_urv'))
    rules = (
        Rule(movie_Extractor, callback='parse_movie'),
    )

    def __init__(self):
        super(ImdbSpider, self).__init__()

    def parse_movie(self, response):
        loader = ItemLoader(item=MovieItem(), response=response)
        loader.add_xpath(
            'name',
            '//div[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/h1/text()')
        loader.add_xpath('year', "//h1/span[@id='titleYear']/a/text()")
        loader.add_xpath(
            'rate', "//div[@id='title-overview-widget']/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()")
        loader.add_xpath(
            'director', "//div[2]/div[1]/div[2]/span/a/span/text()")
        loader.add_xpath(
            'director', "//div[3]/div[1]/div[2]/span/a/span/text()")
        loader.add_xpath(
            'storyline', "//div[@id='titleStoryLine']/div[1]/p/text()")
        user_review_url = response.xpath(
            "//div[@id='titleUserReviewsTeaser']/div/div[3]/a[2]/@href").extract()
        item = loader.load_item()
        user_review_another_url = response.xpath(
            "//div[@id='titleUserReviewsTeaser']/div/div[2]/a[2]/@href").extract()
        if user_review_url or user_review_another_url:
            full_url = 0
            if not user_review_another_url:
                full_url = urljoin(response.url, user_review_url.pop())
            elif not user_review_url:
                full_url = urljoin(response.url, user_review_another_url.pop())
            request = Request(urljoin(response.url, full_url),
                              callback=self.parse_audience_review)
            request.meta['item'] = item
            return request
        return item

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
        item = response.meta['item']
        item['audience_review'] = []
        for title_item, author_item, time_item, content_item, usage_item in result:
            audience_review = {}
            audience_review['title'] = title_item
            audience_review['author'] = author_item
            audience_review['time'] = time_item
            audience_review['content'] = content_item
            audience_review['usage'] = usage_item
            item['audience_review'].append(audience_review)
        return item
