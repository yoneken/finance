# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class FinanceItem(Item):
	date = Field()
	Open = Field()
	High = Field()
	Low = Field()
	Close = Field()
	Volume = Field()
	AdjClose = Field()
	pass
