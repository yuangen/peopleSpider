# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy.http import Request
from peopleSpider.items import PeoplespiderItem
import re
import datetime
import urllib
import urllib3


class XinhuaSpider(scrapy.Spider):
    name = "xinhua"
    allowed_domains = ["xinhuanet.com"]
    start_urls = ['http://www.xinhuanet.com/']

    def parse(self, response):
        today = datetime.datetime.now()
        soup = BeautifulSoup(response.body,'lxml')
        links = soup.findAll('a',{'href':re.compile(r'http:\/\/www\.xinhuanet\.com\/(([a-z]+)|(politics\/leaders))\/2018\-%s\/%s.*\.htm$'%(today.strftime('%m'), today.strftime('%d')))})
        print(len(links))
        with open('link.txt','w') as f:
            for link_item in links:
                f.write(link_item.get('href'))
                f.write('\n')
                url_item = link_item.get('href').strip()
                yield Request(url_item, self.parse_content)
                time.sleep(1)

    def parse_content(self,response):
        item = PeoplespiderItem()
        soup = BeautifulSoup(response.body,'lxml')
        if soup.find('div',{'class':'h-title'}):
            title = soup.find('div',{'class':'h-title'}).getText().replace('\n','').replace('\r','')
            author = ''
            # author = soup.find('p',{'class':'author'}).getText().strip()
            source = ''
            if soup.find('em',{'id':'source'}):
                source = soup.find('em',{'id':'source'}).getText().replace('\n','').replace('\r','')
            else:
                source = '新华网'
            content = soup.find('div',{'id':'p-detail'}).getText().replace('\n','').replace('\r','')
            comment = ''
            time.sleep(1)
            today = datetime.datetime.now()

            item = PeoplespiderItem()
            item['news_title'] = title
            item['news_author'] = author
            item['news_time'] = today.strftime('%Y-%m-%d')
            item['news_content'] = content
            item['news_source'] = source
            item['news_comment'] = comment

            # print(item)
            yield item

        else:
            print('--------------------------------无法解析url-----------------------------------')
            with open('unrelink.txt','a') as f:
                f.write(response.url)
