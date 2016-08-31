#! /usr/bin/env python3
# coding:utf-8
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver


class HtmlParser(object):
    """Documentation for HtmlPa

    """

    def __init__(self):
        phantomjsPath = input(
            "Please input the path of where you install phantomjs: ")
        super(HtmlParser, self).__init__()
        self.driver = webdriver.PhantomJS(
            executable_path=phantomjsPath)  # path of phantomjs

    def parse_info(self, page_url):
        if page_url is None:
            return
        self.driver.get(page_url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')  # parse html
        new_mminfo_urls = self._get_new_mmsinfo_urls(page_url, soup)
        new_mminfo_list = self._get_new_info_data(soup)
        # print(new_mminfo_urls)
        return new_mminfo_urls, new_mminfo_list

    def _get_new_mmsinfo_urls(self, page_url, soup):
        new_mminfo_urls = set()
        links = soup.findAll(
            "a", {"href": re.compile("\/\/.*htm\?(userId=)\d*")})
        for link in links:
            new_url = link['href']
            # it is something tricky that the original url is relative url ,so
            # use urljoin to change it to absolute url
            new_full_url = urljoin(page_url, new_url)
            new_mminfo_urls.add(new_full_url)
        return new_mminfo_urls

    def _get_new_image_urls(self, page_url, soup):
        new_image_url = set()
        imagesUrl = soup.findAll(
            "img", {"data-ks-lazyload": re.compile(".*\.jpg")})
        for imageUrl in imagesUrl:
            new_url = imageUrl['data-ks-lazyload']
            new_full_url = urljoin(page_url, new_url)
            new_image_url.add(new_full_url)  # same as above
        return new_image_url

    def _get_new_info_data(self, soup):
        mminfo_list = []
        info_nodes = soup.findAll('div', class_="info")
        for info_node in info_nodes:
            res_mminfo_data = {}
            # print(info_node.find('name'))
            res_mminfo_data['info'] = info_node.get_text().strip('\n')
            mminfo_list.append(res_mminfo_data)
        # city_node =
        # soup.find('div', class_="info").find("span", class_="city")
        # res_mminfo_data['city'] = city_node.get_text()
        return mminfo_list

    # def get_new_image_data(self, page_url, soup):
        # data=
