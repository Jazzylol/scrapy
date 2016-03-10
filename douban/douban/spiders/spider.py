# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import douban
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import BaseSpider


class DoubanSpider(BaseSpider):
	name = "douban"
	allowed_domain = ["movie.douban.com"]
	start_urls = []

	def start_request(self):
		file_object = open("movie_name.txt", 'r')
		try:
			url_head = "http://movie.douban.com/subject_search?search_text="
			for line in file_object:
				self.start_urls.append(url_head + line)
			for url in self.start_urls:
				yield self.make_requests_from_url(url)
		finally:
			file_object.close()

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		movie_link = hxs.select('//*[@id="content"]/div/div[1]/div[2]/table[1]/tr/td[1]/a/@href').extract()
		if movie_link:
			yield Request(movie_link[0], callback=self.parse_item)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		movie_name = hxs.select("//div[@id='content']/h1/span[1]/text()").extract()
		movie_director = hxs.select("//div[@id='info']/span[1]/span[2]/a/text()").extract()
		movie_writer = hxs.select("//div[@id='info']/span[2]/span[2]/a/text()").extract()
		# 暂时就写3个
		item = douban.douban.items.DoubanItem()
		item['movie_name'] = ''.join(movie_name).strip().replace(
			',', ';').replace('\'', '\\\'').replace('\"', '\\\"').replace(':', ';')
		item['movie_director'] = movie_director[0].strip().replace(',', ';').replace(
			'\'', '\\\'').replace('\"', '\\\"').replace(':', ';') if len(movie_director) > 0 else ''
		item['movie_writer'] = ';'.join(movie_writer).strip().replace(',', ';').replace(
			'\'', '\\\'').replace('\"', '\\\"').replace(':', ';')

		yield item
