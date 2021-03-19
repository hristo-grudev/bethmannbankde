import json

import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import BethmannbankdeItem
from itemloaders.processors import TakeFirst

import requests

url = "https://www.bethmannbank.de/webcontent/api/components?start=0&pageSize=999999&contentType=gROWNieuwsbericht&operation=or&sort=date&lang=de&keywords=10654-79223"

payload={}
headers = {
  'authority': 'www.bethmannbank.de',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'accept': 'application/json',
  'app-id': 'ODA',
  'authorization': 'Basic T0RBOnBvZGF1c2Vyc2VjcmV0MjAyMA==',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.bethmannbank.de/de/news-und-presse/pressemitteilungen/index.html',
  'accept-language': 'en-US,en;q=0.9,bg;q=0.8',
  'cookie': 'ak_bmsc=A7BDDD35131FBB261A152A3F906B31E65435A147161900005B4A5460EC9C0234~pl6pGUZxyzX0j7FLX7xF9UKzsi+flO/5wg28N0anAhICAkk1W52+OdFCB3pdcrEq0904Bs7jci3+0bNIreE/JX7iQ8U+uXVqEPa39HKcurcw0u0L+PTpYD1DeOPVEipm/JPLBp9vD8hZMkDl7P1fW0cWhnEQPM6IkgSocK+PkvsVkUy8BkQhxH/oGBFZQPTy9ZjCiE/a9E1oye1lcgvxMy/vEtt1P8zwg7pueb4joRCX4=; at_check=true; UVID=d00398be-d4ac-48ab-a98f-8beed0008997; s_fid=3C826D605D8E793F-3F0FC034C9C938F7; s_cc=true; CONSENTMGR=consent:true%7Cts:1616136804667; Homepage=news-und-presse; s_sq=%5B%5BB%5D%5D; utag_main=v_id:01784942785c005c54350bf4898c03071002906900bd0$_sn:2$_se:1$_ss:1$_st:1616143449891$vapi_domain:bethmannbank.de$ses_id:1616141649891%3Bexp-session$_pn:1%3Bexp-session; mbox=PC#ff22ef4ccb4b49288c06b711c0e83380.37_0#1679386451|session#f0fcbd15620c472083ec180c30bc6c50#1616143510; mboxEdgeCluster=37; JSESSIONID=3FF2830DB39F4D43F9CCFF1476791E5A; bm_sv=6B6ADD3F1D35F72E266AF6BE880E5352~nTuAH56+OEPCCIOdsbmnvTD5C3kXYmQZPhpT6ckCiED7V1+eBxDrUNU18QZMcG7rtuEwzT8ca0BxGvEmJDmuHoZ270pODoYSyT+bHfOKPE2W8jUn7rmq44jnw3vaRAPVUPvfvVJE1scIWIzWKihzpOYAKr5x1wg4UQEzB9GHI5I=; bm_sv=6B6ADD3F1D35F72E266AF6BE880E5352~nTuAH56+OEPCCIOdsbmnvTD5C3kXYmQZPhpT6ckCiED7V1+eBxDrUNU18QZMcG7rtuEwzT8ca0BxGvEmJDmuHoZ270pODoYSyT+bHfOKPE2lmHQWZZobSajV+0mQ1bUxl/VqleoX17UL1pW+6+L/QRKLkl3rFtEyt89ljV8pI1M='
}


class BethmannbankdeSpider(scrapy.Spider):
	name = 'bethmannbankde'
	start_urls = ['https://www.bethmannbank.de/de/news-und-presse/pressemitteilungen/index.html']

	def parse(self, response):
		data = requests.request("GET", url, headers=headers, data=payload)
		raw_data = json.loads(data.text)
		for post in raw_data:
			title = post['title']
			date = post['newsMetadata']["date"]
			description = remove_tags(post['paragraphs'][0]['text'])

			item = ItemLoader(item=BethmannbankdeItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
