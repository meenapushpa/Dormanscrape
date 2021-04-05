# dormanproduct/crawl.py
import sys
import imp
import os
import logging
from urllib.parse import urlparse
from datetime import datetime

from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Need to "mock" sqlite for the process to not crash in AWS Lambda / Amazon Linux
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")

def is_in_aws():
    return os.getenv('AWS_EXECUTION_ENV') is not None

def crawl(settings={}, spider_name="dorman", spider_kwargs={}):
    project_settings = get_project_settings()
    spider_loader = SpiderLoader(project_settings)
    spider_cls = spider_loader.load(spider_name)
    try:
        if spider_kwargs.get("input"):
                spider_key = spider_kwargs.get("input")
    except Exception:
        logging.exception("Spider or kwargs need input csv file to start.")
    if is_in_aws():
        settings['HTTPCACHE_DIR'] = "/tmp"
        feed_uri = f"s3://{os.getenv('FEED_BUCKET_NAME')}/%s.json'%datetime.utcnow().strftime('%Y-%d-%mT%H-%M-%S').json"
    settings['FEED_URI'] = feed_uri
    process = CrawlerProcess(project_settings)
    process.crawl(spider_cls,spider_key)
    process.start()

