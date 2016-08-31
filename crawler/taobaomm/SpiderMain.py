#!/usr/bin/env python3
# coding:utf-8
# __author__="__samray__"
import UrlManager
import HtmlDownloader
import HtmlOutputer
import HtmlParser


class SpiderMain(object):
    """Documentation for SpiderMain

    """

    def __init__(self):
        super(SpiderMain, self).__init__()
        self.urls = UrlManager.UrlManager()
        self.downloader = HtmlDownloader.HtmlDownloader()
        self.parser = HtmlParser.HtmlParser()
        self.outputer = HtmlOutputer.HtmlOutputer()

    def crawle(self, root_url):
        # count = 1
        # self.urls.add_new_mminfo_url(root_url)
        # while self.urls.has_new_url():
        # try:
        # new_url = self.urls.get_new_url()
        new_urls, new_data = self.parser.parse_info(root_url)
        # self.urls.add_new_urls(new_urls)
        self.urls.add_new_mminfo_urls(new_urls)
        self.outputer.collect_data_dict(new_data)
        self.outputer.collect_urls(new_urls)
        # if count == 2:
        # break
        # count = count + 1
        # except Error as e:
        # print("crawle failed")
        self.outputer.output_text()
if __name__ == "__main__":
    root_url = "https://mm.taobao.com/search_tstar_model.htm?"
    obj_spider = SpiderMain()
    obj_spider.crawle(root_url)
