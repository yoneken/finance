# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter

class FinancePipeline(object):
	def __init__(self):
		self.files = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		file = open('%s_stock.csv' % spider.code, 'w+b')
		self.files[spider] = file
		self.exporter = CsvItemExporter(file, 
				fields_to_export=['date','Open','High', 'Low', 'Close', 'Volume', 'AdjClose'])
		self.exporter.start_exporting()

	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
