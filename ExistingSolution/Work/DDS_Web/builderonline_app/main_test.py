import csv
import os
import requests
import time

from lxml.html import fromstring
from random import randint

proxies = []
proxy_index = 0


def get_proxies():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(dir_path + '/proxy_http_ip.txt', 'r') as fp:
        for line in fp:
            proxies.append(line.strip())

    global proxy_index
    proxy_index = randint(0, len(proxies) - 1)
    print("proxy start index: " + str(proxy_index))


def request_by_proxy(url, start_index):
    global proxies
    global proxy_index

    if abs(proxy_index - start_index) > 2:
        return "URL_ERROR"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    }
    # headers['cookie'] = cookie

    proxy = proxies[proxy_index]
    proxy_index = proxy_index + 1
    if proxy_index >= len(proxies):
        start_index = 0 - abs(proxy_index - start_index)
        proxy_index = 0

    try:
        # response = requests.get(url, headers=headers, timeout=10)
        response = requests.get(url, proxies={"https": "https://" + proxy}, headers=headers, timeout=10)
        # response = requests.get(url, proxies={"https": "https://" + proxy_user + ":" + proxy_pass + "@" + proxy}, headers=headers, timeout=10)

        if response.status_code == 404:
            return "URL_ERROR"
        elif response.status_code != 200:  # or response.url != url
            raise Exception("Proxy Error")

    except Exception as err:
        print("Error :" + str(err))
        response = request_by_proxy(url, start_index)

    return response


def main():
    get_proxies()

    output_file = "top_builders.csv"
    urls = ['https://www.builderonline.com/builder-100/builder-100-list/2020/',
            'https://www.builderonline.com/builder-100/builder-100-list/2020/?next=true']

    i = 0
    while i < len(urls):
        try:
            response = request_by_proxy(urls[i], proxy_index)

            html = fromstring(response.content)
            rows = html.xpath('//table/tbody/tr/td[2]/a')
            if len(rows) == 0:
                print("Error: Your identification is blocked")
                break

            builders = []
            for row in rows:
                try:
                    item = {}
                    href = row.get("href")

                    response = request_by_proxy(href, proxy_index)
                    html = fromstring(response.content)

                    item['Company'] = html.xpath('//h1[contains(@class, "firm-name")]')[0].text
                    item['address'] = html.xpath('//span[contains(@itemprop, "streetAddress")]')[0].text.strip()
                    item['city'] = html.xpath('//span[contains(@itemprop, "addressLocality")]')[0].text
                    item['state'] = html.xpath('//span[contains(@itemprop, "addressRegion")]')[0].text
                    item['phone'] = html.xpath('//div[@class="primary-contact-info"]/p[contains(@class, "phone")]')[0].text
                    item['CEO'] = html.xpath('//div[@class="firm-details"]/div[4]/text()[2]')[0].strip()
                    item['specialites'] = ', '.join(html.xpath('//div[contains(@class,"specialities")]//a[@class="filter-link-blue"]/text()'))
                    item['Services'] = ', '.join(html.xpath('//div[contains(@class,"services")]//a[@class="filter-link-blue"]/text()'))
                    item['Closings_2019'] = html.xpath('//div[@class="revenue"]//p[1]/text()')[0].strip()
                    item['Closings_2018'] = html.xpath('//div[@class="revenue prev"]//p[1]/text()')[0].replace('Closings 2018:', '').strip()
                    item['Revenue_2019'] = html.xpath('//div[@class="revenue"]//p[3]/text()')[0].strip()
                    item['Revenue_2018'] = html.xpath('//div[@class="revenue prev"]//p[2]/text()')[0].replace('Revenue 2018:', '').strip()
                    item['Condos_for_sale'] = html.xpath('//dl[1]/dd[1]')[0].text
                    item['Other_for_sale'] = html.xpath('//dl[1]/dd[2]')[0].text
                    item['Detached_for_sale'] = html.xpath('//dl[1]/dd[3]')[0].text
                    item['Attached_for_sale'] = html.xpath('//dl[2]/dd[1]')[0].text
                    item['Product_mix'] = html.xpath('//dl[2]/dd[2]')[0].text
                    item['Regions'] = html.xpath('//dl[2]/dd[3]')[0].text
                    item['FIRM_DESCRIPTION'] = html.xpath('//section[contains(@class,"firm-description")][2]//text()[2]')[0].strip()

                    builders.append(item)
                except:
                    pass

            if i == 0:
                mode = 'w'
            else:
                mode = 'a+'

            with open(output_file, mode, encoding='utf-8', newline='') as of:
                writer = csv.DictWriter(of, fieldnames=['Program_Name', 'Company_Name', 'Program_Version'], delimiter='|')
                for item in builders:
                    writer.writerow(item)
        except Exception as e:
            print("Error: " + str(e))
            break


if __name__ == "__main__":
    print("Start! : " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

    main()

    print("End! : " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
