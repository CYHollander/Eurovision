from scrapy import Spider, Request
import re
#from eurovision.items import eurovisionItem

class EurovisionSpider(Spider):
	name = 'EV'
	allowed_urls = ['https://en.wikipedia.org']
	end_year=2019

	def start_requests(self):
		for year in range(1956, self.end_year):
			request= Request(url ='https://en.wikipedia.org/wiki/Eurovision_Song_Contest_'+str(year),callback=self.parse)
			request.meta['year'] = year
			yield request

	def parse(self, response):
		filename = 'Eurovision%s.html' % str(response.meta['year'])
		with open(filename, 'wb') as f:
			f.write(response.body)
		self.log('Saved file %s' % filename)