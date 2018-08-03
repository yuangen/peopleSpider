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

class PeopleSpider(scrapy.Spider):
    name = "people"
    allowed_domains = ["people.com.cn"]
    start_urls = ['http://www.people.com.cn/']

    def parse(self, response):
        today = datetime.datetime.now()
        soup = BeautifulSoup(response.body,'lxml')
        links = soup.findAll('a',{'href':re.compile(r'http:\/\/[a-z]+\.people\.com\.cn\/n[1|2]\/2018\/%s.*\.html$'%(today.strftime('%m%d')))})
        print(len(links))
        with open('link.txt','w') as f:
            for link_item in links:
                f.write(link_item.get('href'))
                f.write('\n')
                url_item = link_item.get('href').strip()
                yield Request(url_item, self.parse_content)
                time.sleep(1)
        # url_item = links[0].get('href').strip()
        # yield Request(url_item,self.parse_content)

    def parse_content(self,response):
        soup = BeautifulSoup(response.body,'lxml')
        if soup.find('div',{'class':'clearfix w1000_320 text_title'}):
            title = soup.find('div',{'class':'clearfix w1000_320 text_title'}).find('h1').getText().replace('\n','').replace('\t','')
            author = soup.find('p',{'class':'author'}).getText().strip()
            source = soup.find('div',{'class':'fl'}).find('a').getText()
            content = soup.find('div',{'class':'box_con'}).getText().replace('\n','').replace('\t','')
            comment_url = soup.find('div',{'class':'message'}).find('a').get('href')
            time.sleep(1)
            yield Request(comment_url,self.parse_comment,meta={ 'title': title,
                                                                'author': author,
                                                                'source': source,
                                                                'content': content,
                                                                })
        # print(title)
        # print(author)
        # print(source)
        # print(content)
        # print(comment_url)
        else:
            print('--------------------------------无法解析url-----------------------------------')
            with open('unrelink.txt','a') as f:
                f.write(response.url)


    def parse_comment(self,response):
        time.sleep(1)
        soup = BeautifulSoup(response.body,'lxml')
        # if soup.find('span',{'class':'replayNum'}):
        #     print('yes')
        # else:
        #     print('no')
        cmt_num = soup.find('span',{'class':'replayNum'}).getText()
        print(cmt_num)
        all_comments = ''
        comment_list = []
        if cmt_num != '0':
            com_list = soup.find('ul',{'class':'subUL'}).findAll('a',{'class':'treeReply'})
            for item in com_list:
                comment_list.append(item.getText().strip())
                # print(item.getText().strip())
            all_comments = ';'.join(comment_list)
            all_comments = all_comments.replace('\n','').replace('\t','')
            print(all_comments)
        else:
            all_comments = ''

        today = datetime.datetime.now()

        item = PeoplespiderItem()
        item['news_title'] = response.meta['title']
        item['news_author'] = response.meta['author']
        item['news_time'] = today.strftime('%Y-%m-%d')
        item['news_content'] = response.meta['content']
        item['news_source'] = '人民网'
        item['news_comment'] = all_comments

        # print(item)
        yield item
