# coding: utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import datetime
from scrapy.http import Request
import re

from finance.items import FinanceItem

class YahooFinanceSpider(BaseSpider):
	name = 'yahoo_finance'
	allowed_domains = [
		'stocks.finance.yahoo.co.jp', 
		'info.finance.yahoo.co.jp'
	]
	page = 1
	items = []
	#reg = re.compile("(\\d+)〜(\\d+)件/(\\d+)件中")
	reg = re.compile("(\\d+)\\D+(\\d+)\\D+(\\d+)\\D+")
	url = 'http://info.finance.yahoo.co.jp/history/?code=%s&sy=2010&sm=1&sd=1&tm=d&p=%d'
	code = ''
	#start_urls = [
	#	'http://stocks.finance.yahoo.co.jp/stocks/history/?code=998407.O',
	#	'http://info.finance.yahoo.co.jp/history/?code=7203.T'
	#]

	def __init__(self, code='7203.T'):
		self.start_urls = [self.url % (code, self.page)]
		self.code = code

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		sites = hxs.select('//table[@class="boardFin yjSt marB6"]/tr')
		#items = []
		for site in sites[1:]:
			item = FinanceItem()
			data = site.select('td/text()').extract()
			if len(data) != 7:
				continue
			d = datetime.datetime.strptime(data[0].encode('utf-8'), "%Y年%m月%d日")
			#item['date'] = d.strftime("%m/%d/%Y")
			item['date'] = d.strftime("%Y-%m-%d")
			item['Open'] = data[1].replace(',','')
			item['High'] = data[2].replace(',','')
			item['Low'] = data[3].replace(',','')
			item['Close'] = data[4].replace(',','')
			item['Volume'] = data[5].replace(',','')
			item['AdjClose'] = data[6].replace(',','')
			self.items.append(item)

		# Next page?
		prs = hxs.select('//span[@class="stocksHistoryPageing yjS"]/text()').extract()
		#print prs[0].encode('utf-8')
		res = self.reg.match(prs[0].encode('utf-8'))
		print res.groups()

		if res.group(2) == res.group(3):
			return self.items
		else:
			self.page += 1
			return Request(self.url % (self.code, self.page))

