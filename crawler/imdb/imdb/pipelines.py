# -*- coding: utf-8 -*-
import pymongo
import json
import codecs
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ImdbPipeline(object):

    def __init__(self):
        self.file = codecs.open('imdb.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line.strip(''))
        return item

    def spider_closed(self, spider):
        self.file.close()


class MongodbPipeline(object):
    """Documentation for MongodbPipel

    """

    def __init__(self):
        super(MongodbPipeline, self).__init__()

        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']

        )
        db = connection[settings['MONGODB_DB']]
        self.colletion = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.colletion.insert(dict(item))
            log.msg("Audience Review added to Mongodb database",
                    level=log.DEBUG, spider=spider)
        return item
