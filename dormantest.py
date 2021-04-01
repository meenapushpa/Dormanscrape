# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import datetime
import calendar
from urllib.parse import urljoin
from csv import DictReader
from lxml.html import fromstring
import freeproxy
import os.path
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url_template = 'https://www.dormanproducts.com/gsearch.aspx?type=oesearch&origin=oesearch&q={}'
proxyurl = str(freeproxy.Proxy())
headers = {
    'host': 'www.dormanproducts.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}

def log(event,val=None):
    d = datetime.datetime.now().strftime("%x %H:%M:%S")
    if val:
        print("[Dorman Logs] :: " + str(d) + " :: " + event +  " :: " + val)
    else:
        print("[Dorman Logs] :: " + str(d) + " :: " + event)

class Dorman(object):

	def scrape(self,response):
		#response=request(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		resultcount=soup.find_all('span','lblResultCount')
		if resultcount != None:
			results=soup.find(class_='col-lg-9 col-sm-8 col-xs-12')
			str = results.find_all('div', 'row searchResults')
			rows,list,newlist=[],[],[]
			for i in str:
				itemname=i.find(class_='item-name').text
				iteminfo=i.find('h4').text
				itemsum=i.find('p').text
				tableval=i.find(class_='table-responsive')
				for tr in tableval.select('tr'):
					rows.append([td.get_text(strip=True) for td in tr.select('th, td')])
				for k in rows:
					for j in k:
						list.append(j)
				browseval=i.find_all('a', {'class': 'btn btn-darkgrey centered detail-btn', 'href': True})
				oedetail=self.detailpage(browseval,proxyurl)
				oedetails=[]
				for oe in oedetail:
					oedetails.append(':'.join(oe))
				product_details = {
						'ProductName': itemname,
						'ProductInfo': iteminfo,
						'ProductSummary': itemsum,
						'Cross': list[0],
						'OE': list[1],
						'Mfr Name': list[2],
						'OE Numbers': oedetails
					}
				newlist.append(product_details)
            file_exists = os.path.isfile(filename)
			with open('DormanScrapedData.csv', 'w') as csvfile:
				fieldnames = [ 'ProductName', 'ProductInfo', 'ProductSummary','Cross', 'OE','Mfr Name','OE Numbers']
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator='\n', quoting=csv.QUOTE_ALL)
                if not file_exists:
                    writer.writeheader()
				for i in newlist:
					writer.writerow(i)
                    csvfile.truncate()
		else:
			print('No Results............')

	def detailpage(self,input,proxy):
		detrows,detlist=[],[]
        try:
            for anchor in input:
    			url = urljoin('https://www.dormanproducts.com/',anchor['href'])
    			res=requests.get(url,headers=headers,proxies={"http": proxy, "https": proxy})
    			soup = BeautifulSoup(res.text, 'html.parser')
    			section=soup.find(id='productOE')
    			dettable=section.find(class_='table table-hover table-dorman table-striped')
    			for tr in dettable.select('tr'):
                    detrows.append([td.get_text(strip=True) for td in tr.select('th,td')])
        except:
            proxynexturl = str(freeproxy.Proxy())
            log('Changing the PROXY [ ' + str(proxynexturl) + ' ] and trying Dorman interchangecode entries')
            response = self.detailpage(input, proxynexturl)
        return detrows

	def responsepage(self,outcode,proxy):
		url=url_template.format(outcode)
        try:
            response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy},verify=False)
        except:
            proxynexturl = str(freeproxy.Proxy())
            response = self.responsepage(outcode, proxynexturl)
		return response

if __name__ == '__main__':
	dr=Dorman()
    with open('Input_2_OEo.csv', 'r', encoding='utf8') as file:
        csv_dict_reader = DictReader(file)
        for row in csv_dict_reader:
            input=row['Compressed Old number']
            print(input,proxyurl)
            res = dr.responsepage(input,proxyurl)
            dr.scrape(res)
