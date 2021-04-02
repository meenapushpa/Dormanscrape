# -*- coding: utf-8 -*-
import scrapy


class DormanSpider(scrapy.Spider):
    name = 'dorman'
    allowed_domains = ['dormanproducts.com']
    start_urls = ['http://dormanproducts.com/']
    url_template='https://www.dormanproducts.com/gsearch.aspx?type=oesearch&origin=oesearch&q={}'

    def __init__(self, p=None, fn=None, *args, **kwargs):
        super(DormanSpider, self).__init__(*args, **kwargs)
        if not p and not fn:
            raise ValueError('You have to input either product code via the command line (-o) or use a filename (-fn)!')
        if p:
            self.productcodes = [x.strip().lower() for x in p.split(',')]
        else:
            with open(fn,'r') as fp:
                self.productcodes = [x.replace('\n','') for x in fp.readlines()]
            logging.debug('outcodes loaded...{}'.format(self.productcodes))

    def start_requests(self):
        # generate url and launch url for each productcode.
        for code in self.productcodes:
            url = self.url_template.format(code)
            yield scrapy.Request(url, callback=self.parse_listing)

    def parse_listing(self, response):
        logging.debug('parsing listings...{}'.format(response.url))
        sel = Selector(response)
        links = sel.xpath('//div[@class="row searchResults"]').extract()
        print(links)
        # find all the listings on the page and send them to a parser
        for url in links:
            url = urljoin(response.url,url).split('?')[0].strip()
            if 'expired' in url:
                logging.debug('skipping expired property: {}'.format(url))
                continue
            yield scrapy.Request(url, callback=self.parse_property)
        next_page = sel.xpath('//*[@id="__next"]/div[6]/div/main/div[2]/div[3]/ul/li[5]/a/@href').extract()
        if next_page:
            next_page = urljoin(response.url,next_page[0])
            yield scrapy.Request(next_page, callback=self.parse_listing)

    def parse(self, response):
        pass
