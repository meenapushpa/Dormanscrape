# -*- coding: utf-8 -*-

# Scrapy settings for dormanproduct project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
import sys
from datetime import datetime

BOT_NAME = 'dormanproduct'

SPIDER_MODULES = ['dormanproduct.spiders']
NEWSPIDER_MODULE = 'dormanproduct.spiders'

USER_AGENT_LIST = "./misc/useragents.txt"
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400,
}
LOG_LEVEL = 'WARNING'

CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN = 20

DOWNLOAD_TIMEOUT = 30
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 404, 408]


FEED_FORMAT = 'json'
#FEED_URI = 'data/%s.json' % datetime.utcnow().strftime('%Y-%d-%mT%H-%M-%S')  # WHERE to store the export file

REDIRECT_ENABLED = True
REFERER_ENABLED = False

COOKIES_ENABLED = False
COOKIES_DEBUG = False

PROXY_LIST = ['http://15.185.193.6:3128/', 'http://165.225.77.47:9443/']
if PROXY_LIST:
    DOWNLOADER_MIDDLEWARES['dormanproduct.middlewares.RetryMiddleware'] = 200
    DOWNLOADER_MIDDLEWARES['dormanproduct.middlewares.ProxyMiddleware'] = 100

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 60 * 60 * 24 * 7
HTTPCACHE_DIR = 'httpcache'
CLOSESPIDER_PAGECOUNT = 32
