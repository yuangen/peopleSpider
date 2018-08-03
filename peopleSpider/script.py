# -*- coding: utf-8 -*-
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# import time
# process = CrawlerProcess(get_project_settings())
# process.crawl('people')
# process.crawl('xinhua')
# # process.crawl('C_spider')
# process.start()
import time
import os
from openpyxl import Workbook
import datetime


print('the first spider')
os.system("scrapy crawl people")
time.sleep(600)
print('the second spider')
os.system("scrapy crawl xinhua")

