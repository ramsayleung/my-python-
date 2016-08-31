#!/usr/bin/env python3
# coding:utf-8
# __author__='__samray__'


class UrlManager(object):
    """Documentation for URLManager

    """

    def __init__(self):
        super(UrlManager, self).__init__()
        self.mminfo_urls = set()  # urls which are being crawled
        self.mmimage_urls = set()  # urls which have been crawled

    def add_new_mminfo_url(self, url):
        if url is None:
            return
        if url not in self.mminfo_urls:
            self.mminfo_urls.add(url)

    def add_new_mmimage_url(self,url):
        if url is None:
            return
        if url not in self.mmimage_urls:
            self.mmimage_urls.add(url)

    def add_new_mmimage_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_mmimage_url(url)

    def add_new_mminfo_urls(self,urls):
        if urls is None or len(urls)==0:
            return
        for url in urls:
            self.add_new_mminfo_url(url)

    def has_new_mmimage_url(self):
        return len(self.mmimage_urls) != 0

    def has_new_mminfo_url(self):
        return len(self.mminfo_urls)!=0

    def get_new_mmimage_url(self):
        new_url = self.mmimage_urls.pop()  # pop a url to crawle
        # crawed url set add the poped url,which means the url has been crawed
        return new_url
    def get_new_mminfo_url(self):
        new_url=self.mminfo_urls.pop()
        return new_url
