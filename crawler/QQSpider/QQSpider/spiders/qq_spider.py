#!/usr/bin/env python
# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.selector import Selector
# from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request
import get_cookie
import get_gtk
import fileinput as fileinput
import sys
import json
from QQSpider.items import QqspiderItem


class QQSpider(CrawlSpider):
    name = 'qq'
    allowed_domains = ["qq.com"]

    def __init__(self):
        self.account = raw_input("input your login account: ")
        self.password = raw_input("input your password: ")
        self.account_for_crawl = raw_input(
            "input the account you want to crawl:")
        self.get_cookie_instance = get_cookie.GetCookie()
        self.get_cookie = self.get_cookie_instance.getCookie(self.account,
                                                             self.password)
        self.get_gtk_instance = get_gtk.GetGtk()
        self.gtk = self.get_gtk_instance.getGTK(self.get_cookie)
        print(self.gtk)

    def start_requests(self):
        return [Request(
            url="http://h5.qzone.qq.com/proxy/domain/alist.photo.qq.com/fcgi-bin/fcg_list_album_v3?g_tk="
            + str(self.gtk) +
            "&callback=shine0_Callback&t=955106858&hostUin=" + \
            str(self.account_for_crawl) + \
            "&uin="+str(self.account) + \
            "&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&format=jsonp&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15&needUserInfo=1&idcNum=0&callbackFun=shine0&_=1474681546872",
            cookies=self.get_cookie,
            callback=self.parse)]

    def parse(self, response):
        response_json = response.body
        # 将得到的请求结果保存到文件
        with open("response.txt", "wt") as tmpWrite:
            tmpWrite.write(response_json)
            # 对response进行修改，变成标准的json文件
        self.replaceAll("response.txt", "shine0_Callback({", "{")
        self.replaceAll("response.txt", ");", "")
        with open("response.txt") as data_file:
            json_formatted = json.load(data_file)

        # album_list_num = len(json_formatted["data"]["albumListModeSort"])
        for album_list in json_formatted["data"]["albumListModeSort"]:
            album_id = album_list['id']
            total_photo = album_list['total']
            print(album_id, total_photo)
            #qq空间最多只会返回200条数据
            counter = 0
            while counter < total_photo:
                image_url = "http://h5.qzone.qq.com/webapp/json/mqzone_photo/getPhotoList2?g_tk=" + \
                            str(self.gtk) +\
                            "&uin="+str(self.account_for_crawl)+"&albumid=" + album_id + "&ps="+str(counter)+"&pn=" + \
                            str(total_photo) +"&password=&password_cleartext=0&swidth=1920&sheight=1080&sid=Pp7O26sWwPQbVfSPlzR0XBaL7ZpyXD9D33d842420201%3D%3D"
                counter += 200
                yield Request(
                    image_url,
                    callback=self.parse_image,
                    cookies=self.get_cookie, )

    def parse_image(self, response):
        # print(response.body)
        item = QqspiderItem()
        with open("photos.json", "wt") as photos_json:
            photos_json.write(response.body)
        with open("photos.json") as photos_json:
            photos = json.load(photos_json)
        album_name = photos['data']['album']['name']
        item['album_name'] = album_name
        image_urls = []
        for key in photos['data']['photos'].keys():
            for photo in photos['data']['photos'][key]:
                image_url = photo['1']['url']
                image_urls.append(image_url)
        item['image_urls'] = image_urls
        yield item

    def replaceAll(self, filename, searchExp, replaceExp):
        for line in fileinput.input(files=(filename), inplace=1):
            # for line in f:
            if searchExp in line:
                line = line.replace(searchExp, replaceExp)
            sys.stdout.write(line)
