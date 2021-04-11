# dormanproduct/crawl.py
import sys
import imp
import os
import logging
from urllib.parse import urlparse
from datetime import datetime
import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings


# Need to "mock" sqlite for the process to not crash in AWS Lambda / Amazon Linux
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")


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


def is_in_aws():
    return os.getenv('AWS_EXECUTION_ENV') is not None


def crawl(settings={}, spider_name="dorman", spider_kwargs={}):
    project_settings = get_project_settings()
    spider_loader = SpiderLoader(project_settings)
    spider_cls = spider_loader.load(spider_name)
    input_parse, split_urls = [], []
    try:
        if spider_kwargs.get("input"):
            spider_key = spider_kwargs.get("input")
            input_parse = inputcodes(spider_key)
            split_urls = chunkIt(input_parse, 10)
    except Exception:
        logging.exception("Spider or kwargs need input csv file to start.")
    if is_in_aws():
        settings['HTTPCACHE_DIR'] = "/tmp"
        feed_uri = f"s3://{os.getenv('FEED_BUCKET_NAME')}/%s.json'%datetime.utcnow().strftime('%Y-%d-%mT%H-%M-%S').json"
        settings['FEED_URI'] = feed_uri
    for index in split_urls:
        def f(q):
            try:
                runner = crawler.CrawlerRunner()
                deferred = runner.crawl(spider_cls, index)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run()
                q.put(None)
            except Exception as e:
                q.put(e)
        q = Queue()
        p = Process(target=f, args=(q,))
        p.start()
        result = q.get()
        print(result)
        p.join()

    if result is not None:
        raise result

