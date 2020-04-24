# -*- coding: utf-8 -*-
import scrapy
import re
import json
from crawler.items import CrawlerImageUrlItem
import requests

IMAGE_NAME = re.compile(r'.+.(jpg|png|bmp|gif|tiff|jpeg)', re.IGNORECASE)

class SougouSpider(scrapy.Spider):
    name = 'sougou'
    allowed_domains = ['https://pic.sogou.com']
    start_urls = ['http://pic.sogou.com/']
    
    base_url  = 'http://pic.sogou.com/pics?query={}\
                   &mode=1&start={}&reqType=ajax&reqFrom=result&tn=0'
    
    custom_settings = {
       "USER_AGENT" : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
       "DEFAULT_REQUEST_HEADERS" : {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
           'Referer': 'https://pic.sogou.com/'
       },
       "ITEM_PIPELINES" : {
           'scrapy.pipelines.images.ImagesPipeline':300
       },
       "IMAGES_STORE" : './sougouimage',
       "IMAGES_URLS_FIELD" : 'ImageUrl',
    }
    
    def __init__(self, key=None, *args, **kwargs):
        super(SougouSpider, self).__init__(*args, **kwargs)
        self.key = key
        self.pn = 0

        url = self.base_url.format(key, 0)
        print(url)
        self.start_urls.append(url)

    def parse(self, response):
        data = json.loads(response.text)
        if not data:
            return
        pic_items = data['items']
        for i in pic_items:
            url = i['pic_url']
            item = CrawlerImageUrlItem()
            try:
                item['ImageUrl'] = [url]
            except Exception as e:
                print(e)
            yield item
        
        self.pn += 48
        url = self.base_url.format(self.key, self.key, self.pn)
        yield scrapy.Request(url, callback=self.parse, headers=
            self.settings.get("DEFAULT_REQUEST_HEADERS"), dont_filter=True)
