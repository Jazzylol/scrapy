from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import BaseSpider

from .. import items

class TripSpider(BaseSpider):
	name = "trip"
	allowed_domain = ["www.tripadvisor.cn"]
	start_urls = ["http://www.tripadvisor.cn/Attractions-g308272-Activities-oa90-Shanghai.html"]

	def parse(self, response):
		hss = HtmlXPathSelector(response)
		name = hss.select('//*div[@class="property_title"]/a/text()').extract()
		item = items.TraningItem()
		item['name'] = name
		filename = "D://trip.txt"
		with open(filename, 'wb') as f:
			f.write(response.body)
