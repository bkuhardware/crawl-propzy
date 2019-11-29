# -*- coding: utf-8 -*-
import scrapy

class LandsSpider(scrapy.Spider):
    name = 'lands'
    start_urls = ['https://propzy.vn/mua/ban-dat-nen-tphcm']

    def parse(self, response):
        pass
