# -*- coding: utf-8 -*-
import scrapy
import json
import re
import logging
from urllib.parse import urljoin
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
import boto3
from multiprocessing import Pool
from string import whitespace
import mysql.connector


class DormanSpider(scrapy.Spider):
    name = 'dorman'
    allowed_domains = ['dormanproducts.com']
    start_urls = ['http://dormanproducts.com/']
    url_template = 'https://www.dormanproducts.com/gsearch.aspx?type=oesearch&origin=oesearch&q={}'

    def __init__(self, *args, **kwargs):
        super(DormanSpider, self).__init__(*args, **kwargs)
        self.args = str(args)
        self.index = [x.strip("'([])'").lower() for x in self.args.split(',')]

    def start_requests(self):
        for code in self.index:
            code = code.strip(whitespace + " ' ")
            if code:
                url = self.url_template.format(code)
                print(url)
                yield scrapy.Request(url, callback=self.parse_listing)

    def parse_listing(self, response):
        logging.debug('parsing listings...{}'.format(response.url))
        sel = Selector(response)
        links = sel.xpath('//div[@class="row searchResults"]').extract()
        for i in links:
            parse = Selector(text=i)
            itemname = parse.xpath('//span[@class="item-name"]/text()').get()
            iteminfo = parse.xpath('//h4/text()').get()
            itemsum = parse.xpath('string(//p)').get()
            tablehead = parse.xpath('//table//thead//th/text()').get()
            tablebody = parse.xpath('//table//tbody//th/text()').get()
            tablehead = tablehead.lstrip()
            tabledata = parse.xpath('//table//td/text()').get()
            product_details = {
                'Product Name': itemname,
                'Product Info': iteminfo,
                'Product Summary': itemsum,
                'Cross': tablehead,
                'OE ref': tablebody,
                'Mfr Name': tabledata
            }
            next_page = parse.xpath(
                '//a[@class="btn btn-darkgrey centered detail-btn"]/@href').extract()
            if next_page:
                url = urljoin('https://www.dormanproducts.com/', next_page[0])
                yield scrapy.Request(url, callback=self.detailparse, meta={'details': product_details, 'dont_merge_cookies': True, 'dont_filter': True})

    def detailparse(self, response):
        sel = Selector(response)
        tabledetails = sel.xpath('//section[@id="productOE"]').extract()
        parse1 = Selector(text=tabledetails[0])
        oehead = parse1.xpath('//table//tbody//th//text()').get()
        oedata = parse1.xpath('//table//tbody//td//text()').get()
        oe_details = {
            'OE details': (oehead + ':' + oedata)
        }
        finalresult = response.meta['details']
        finalresult.update(oe_details)
        jsonresults = json.dumps(finalresult)
        item = json.loads(jsonresults)
        print(item)
        self.dbwrite(item)
        yield item

    def dbwrite(self, dbinput):
        insert_list = []
        mydb = mysql.connector.connect(
            host="172.31.53.216",
            user="admin",
            port=3306,
            password="test1234",
            database="dormandb"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO `dormantable` (`Product Name`, `Product Info`,`Product Summary`,`Cross`,`OE ref`,`Mfr Name`,`OEdetails`) VALUES (%s, %s,%s,%s,%s,%s,%s)"
        for i in dbinput.items():
            finalvalue = ''.join(i[1])
            insert_list.append(finalvalue)
        print(insert_list)
        mycursor.execute(sql, insert_list)
        mydb.commit()
        print(mycursor.rowcount, "record(s) sucessfully written to database.")
