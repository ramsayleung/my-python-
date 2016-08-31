#!/usr/bin/env python3
# coding:utf-8
# __author__="__samray__"
from urllib.request import urlopen


class HtmlDownloader(object):
    """Documentation for HtmlDownloader

    """

    def __init__(self):
        super(HtmlDownloader, self).__init__()

    def download(self, url):
        if url is None:
            return None
        response = urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read()
