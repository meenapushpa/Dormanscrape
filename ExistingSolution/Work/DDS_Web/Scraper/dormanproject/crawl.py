# dormanproduct/crawl.py
import sys
import imp
import os
import logging
from urllib.parse import urlparse
from datetime import datetime
import scrapy
import scrapy.crawler as crawler
from scrapy.crawler import CrawlerProcess,CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process, Queue
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy import signals
import time
from pydispatch import dispatcher
from crochet import setup
setup()
def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out


def crawl(itemlist,output_filename,settings={},spider_name='dorman'):
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'scraper.dormanproject.settings'
    project_settings = get_project_settings()
    project_settings.update({
        'DOWNLOAD_DIR': output_filename
        })
    spider_loader = SpiderLoader(project_settings)
    spider_cls = spider_loader.load(spider_name)

    runner = CrawlerRunner(project_settings)
    split_urls = []
    try:
        split_urls = chunkIt(itemlist, 9)
        for index in split_urls:
            print('Iteration -',index)
            configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
            runner.crawl(spider_cls, index)
            time.sleep(60)
        #runner.start()
    
    except Exception as e:
        print(e)
