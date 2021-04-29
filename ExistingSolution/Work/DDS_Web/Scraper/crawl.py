# dormanproduct/crawl.py
import sys
import imp
import os
import logging
from urllib.parse import urlparse
from datetime import datetime
import scrapy
import scrapy.crawler as crawler

from twisted.internet import reactor
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings

def inputcodes(filepath):
    productcodes = []
    with open(filepath, 'r') as fp:
        next(fp)
        productcodes = [x.replace('\n', '') for x in fp.readlines()]
    return productcodes

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def crawl(settings={}, spider_name="dorman",list1,output):
    project_settings = get_project_settings()
    spider_loader = SpiderLoader(project_settings)
    spider_cls = spider_loader.load(spider_name)
    split_urls = []
    try:
        input_parse = inputcodes(filename)
        split_urls = chunkIt(list1, 10)
    except Exception:
        logging.exception("Spider or kwargs need input csv file to start.")
    for index in split_urls:
        print(index, 'Iteration is happening!!!')
        runner = crawler.CrawlerRunner(project_settings)
        runner.crawl(spider_cls, index,output)
