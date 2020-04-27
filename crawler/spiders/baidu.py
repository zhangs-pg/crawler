# -*- coding: utf-8 -*-
import scrapy
import json
from crawler.items import CrawlerImageUrlItem
import requests

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['https://image.baidu.com/']
    #start_urls = ['http://https://image.baidu.com/']
    base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&\
         ipn=rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8&\
         oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={}\
         &s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&\
         force=&pn={}&rn=30&gsm=3c&1587623974357="
    
    custom_settings = {
        "USER_AGENT" : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        "DEFAULT_REQUEST_HEADERS" : {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Referer': 'https://image.baidu.com'
        },
        "ITEM_PIPELINES" : {
            'scrapy.pipelines.images.ImagesPipeline':300
        },
        "IMAGES_STORE" : './baiduimage',
        "IMAGES_URLS_FIELD" : 'ImageUrl',
    }
    

    def __init__(self, key=None, *args, **kwargs):
        super(BaiduSpider, self).__init__(*args, **kwargs)
        self.key = key
        self.pn = 0
        url = self.base_url.format(key, key, 0)
        self.start_urls.append(url)
        
    def parse(self, response):
        try:
            data = json.loads(response.text)
        except Exception as e:
            print(e)
            self.pn += 30
            url = self.base_url.format(self.key, self.key, self.pn)
            yield scrapy.Request(url, callback=self.parse, headers=
                self.settings.get("DEFAULT_REQUEST_HEADERS"), dont_filter=True)
        else:
            if not data:
                return
            objects =data["data"]
            if len(objects[0]) == 0:
                return
            for obj in objects:
                item = CrawlerImageUrlItem()
                try:
                    item['ImageUrl'] = [obj["thumbURL"]]
                except Exception as e:
                    print(e)
                else:
                    yield item
            
            self.pn += 30
            url = self.base_url.format(self.key, self.key, self.pn)
            yield scrapy.Request(url, callback=self.parse, headers=
                self.settings.get("DEFAULT_REQUEST_HEADERS"), dont_filter=True)
