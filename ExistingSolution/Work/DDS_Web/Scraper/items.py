# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DormanprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    partno =scrapy.Field()
    ProductName = scrapy.Field()
    ProductInfo =scrapy.Field()
    ProductSummary = scrapy.Field()
    Cross = scrapy.Field()
    OEref = scrapy.Field()
    MfrName = scrapy.Field()
    Oedetails = scrapy.Field()
    """
    original_part_number = scrapy.Field()
    product_name = scrapy.Field()
    product_info = scrapy.Field()
    application_summary = scrapy.Field()
    cross = scrapy.Field()
    part_no = scrapy.Field()
    manufacturer_name = scrapy.Field()

    #created = models.DateTimeField(auto_now=True)
    """
