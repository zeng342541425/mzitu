# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
import urllib
import os
import requests

class MzSpider(scrapy.Spider):
    name = 'mz'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com/xinggan/']

    def parse(self, response):
    	for i in range(1,162):
    		url="http://www.mzitu.com/xinggan/page/"+str(i)+"/"
    		body=response.body.decode('utf-8','ignore')
    		idmatch="com\/(\d*)"
    		ids=re.compile(idmatch).findall(body)
    		while '' in ids:
    			ids.remove("")
    		for i in range(1,len(ids)):
    			urls="http://www.mzitu.com/"+str(ids[i])
    			# print(urls)
    			headers={
    				"Accept":"*/*",
    				"Accept-Encoding":"gzip,deflate",
    				"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    				"Connection":"Keep-Alive",
    				"Cookie":"Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1514102271;Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1514103534",
    				"Host":"www.mzitu.com",
    				"Referer":urls,
    				"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0",
    				"X-Requested-With":"XMLHttpRequest",
    			}
    			yield Request(url=urls,callback=self.page,headers=headers)

    def page(self,response):
    	imageurl=response.url
    	# print(imageurl)
    	images=response.xpath("//div[@class='pagenavi']/a[last()-1]/span/text()").extract()[0]
    	# print(images)
    	for i in range(1,int(images)):
    		imageurls=imageurl+"/"+str(i)
    		# print(imageurls)
    		headers={
    			"Accept":"*/*",
    			"Accept-Encoding":"gzip,deflate",
    			"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    			"Connection":"Keep-Alive",
    			"Cookie":"Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1514102271;Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1514103534",
    			"Host":"www.mzitu.com",
    			"Referer":imageurls,
    			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0",
    			"X-Requested-With":"XMLHttpRequest",
    		}
    		yield Request(url=imageurls,callback=self.next,headers=headers)

    def next(self,response):
    	imagename=response.xpath("//h2[@class='main-title']/text()").extract()[0]
    	# print(imagename)
    	imageurl=response.xpath("//div[@class='main-image']/p/a/img/@src").extract()[0]
    	# imagename=response.xpath("//div[@class='main-image']/p/a/img/@alt").extract()[0]
    	# print(imageurl)
    	headers = {
    		'Accept':'*/*',
    		'Accept-Encoding':'gzip, deflate',
    		'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    		'Connection':'keep-alive',
    		'Host':'i.meizitu.net',
    		'Referer':imageurl,
    		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
    	}

    	file_path=os.path.join("F:\\imgss",imagename)+'.jpg'
    	# urllib.request.urlretrieve(imageurl,file_path)
    	# 
    	r = requests.get(imageurl,headers=headers)
    	with open(file_path, 'wb') as fd:
    		fd.write(r.content)
    	# print(file_path)

