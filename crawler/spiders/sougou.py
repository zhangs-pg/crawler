# -*- coding: utf-8 -*-
import scrapy


class SougouSpider(scrapy.Spider):
    name = 'sougou'
    allowed_domains = ['https://pic.sogou.com']
    start_urls = ['http://pic.sogou.com/']

    def parse(self, response):
        pass
