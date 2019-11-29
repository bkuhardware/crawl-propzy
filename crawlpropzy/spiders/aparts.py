# -*- coding: utf-8 -*-
import scrapy

class ApartsSpider(scrapy.Spider):
    name = 'aparts'
    start_urls = ['https://propzy.vn/mua/ban-can-ho-chung-cu-tphcm']

    def parse(self, response):
        pass
