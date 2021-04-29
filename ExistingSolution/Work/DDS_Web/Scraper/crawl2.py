from scrapy.crawler import CrawlerProcess,CrawlerRunner
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy import signals
import time
import os
from crochet import setup
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from .pipelines import InMemoryItemStore
from scrapy.utils.project import get_project_settings
from pydispatch import dispatcher 
setup()

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def setup_crawler(index,output_filename,settings={}, spider_name="dorman"):
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'scraper.dormanproject.settings'
    settings=get_project_settings()
    settings.update({
        'DOWNLOAD_DIR': output_filename,
        })
    InMemoryItemStore.pop_items()
    runner = CrawlerProcess(settings)
    spider_loader = SpiderLoader(settings)
    spider_cls = spider_loader.load(spider_name)
    runner.crawl(spider_cls, index)
    time.sleep(10)
    return InMemoryItemStore.pop_items()

def crawl(list1,output_filename):
    print('crawl file',list1)
    #split_urls = chunkIt(list1, 9)
    #final_list=[]
    #for index in split_urls:
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    d=setup_crawler(list1,output_filename)
    return d


