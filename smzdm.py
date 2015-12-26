#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-12-17 09:55:41
# Project: resulttest8




import time
import re
from pyspider.libs.base_handler import *
import json




class Handler(BaseHandler):
    crawl_config = {
    }

    
    def on_start(self):
        self.crawl('http://www.smzdm.com/', callback=self.index_page, age=5*60, auto_recrawl=True)

    
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://www.smzdm.com/p/\d+$", each.attr.href) or re.match("http://haitao.smzdm.com/p/\d+/$",each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
        #self.crawl(response.doc('.pagedown a').attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        
        author = response.doc('.author')
        if author == []:
            fabutime = response.doc('.article_meta:first-child span').text()
        else:
            fabutime = response.doc('.author+span').text()
        
        fabutime = fabutime[3:]
        
        imgList =[]
        
        for each in response.doc('.smallImgList li a').items():
            imgList.append(each.attr.rel)
            
            
        imgjson = json.dumps(imgList)
        
        return {
            "url": response.url,
            "title": response.doc('.article_title').text(),
            "price": response.doc('.article_title span').text(),
            "sale_desc": response.doc('[itemprop="description"]:first-child').text(),
            "product_desc": response.doc('.wiki-box+.inner-block p:first-child').text(),
           # "fabu-time": response.doc('.author+span').text(),
            "fabu_time": fabutime,
           # "now-time": time.strftime( '%Y-%m-%d %X', time.localtime( time.time() ) ),
            "imglist": imgjson,
            "preprice": 'no',
            "start_time": 'no',
            "end_time": 'no',
            "img": response.doc('.article-top-box a img').attr.src,
          
        }
    
    def otherthing(self, task, result):
        if not result or not result['title']:
            return
        
        result['taskid'] = task['taskid']
        result["updatetime"] = time.time()
        
        sql = SQL()
        sql.replace('douban_db',**result)
        
        
        



