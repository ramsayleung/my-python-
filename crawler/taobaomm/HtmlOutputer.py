#! /usr/bin/env python3
# coding:utf-8


class HtmlOutputer(object):
    """Documentation for HtmlOutputer

    """

    def __init__(self):
        super(HtmlOutputer, self).__init__()
        self.datas = []
        self.urls = set()

    def collect_data_dict(self, datas):
        if datas is None:
            return
        self.datas = datas

    def collect_urls(self, urls):
        if urls is None:
            return
        self.urls = urls

    def output_text(self):
        with open("mminfo.txt", 'w+') as fileWrite:
            for data in self.datas:
                fileWrite.write(data['info'] + "\n")
                # fileWrite.write(data['name_city'] + ' ')
            for url in self.urls:
                fileWrite.write(url + "\n")
