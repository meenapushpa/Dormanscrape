# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from urllib.parse import urljoin
from csv import DictReader
import re
from lxml.html import fromstring

def resultpage(url):
	headers = {'host': 'www.dormanproducts.com'}
	proxies = get_proxies()
	print(proxies)
	try:
		for proxy_link in proxies:
		proxy = {
		'http': proxy_link,
		'https': proxy_link
		}
		response = requests.get(url, headers=headers, proxies=proxy,verify=False)
		print('response is....' + response)
		return response

def detailpage(input):
	detrows,detlist=[],[]
	for anchor in input:
		url = urljoin('https://www.dormanproducts.com/',anchor['href'])
		res=resultpage(url)
		soup = BeautifulSoup(res.text, 'html.parser')
		section=soup.find(id='productOE')
		dettable=section.find(class_='table table-hover table-dorman table-striped')
		for tr in dettable.select('tr'):
			detrows.append([td.get_text(strip=True) for td in tr.select('th,td')])
	return detrows

def scrape(response):
	print('entered to scrape the sites......')
	soup = BeautifulSoup(response.text, 'html.parser')
	divtag=soup.find(class_='search-results-headline col-sm-10')
	if divtag != None:
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
			oedetail=detailpage(browseval)
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
		with open('DormanScrapedData.csv', 'w') as csvfile:
			fieldnames = [ 'ProductName', 'ProductInfo', 'ProductSummary','Cross', 'OE','Mfr Name','OE Numbers']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator='\n', quoting=csv.QUOTE_ALL)
			writer.writeheader()
			for i in newlist:
				writer.writerow(i)
	else:
		print('No Results............')

if __name__ == '__main__':
	url_template = 'https://www.dormanproducts.com/gsearch.aspx?type=oesearch&origin=oesearch&q={}'
	with open('Input_2_OEo.csv', 'r', encoding='utf8') as file:
		csv_dict_reader = DictReader(file)
		for row in csv_dict_reader:
			input=row['Compressed Old number']
			print(url_template.format(input))
			res=resultpage(url_template.format(input))
			scrape(res)
