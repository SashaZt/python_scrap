import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MebliSpider(CrawlSpider):
    name = 'mebli'
    start_url = ['https://komfortmebli.com.ua/ua/']
    all_product = LinkExtractor(restrict_xpaths='//div[@class="col-md-9 col-sm-8 col-sm-pull-4 col-md-pull-3"]')
    rule_product_details = Rule(all_product,
                                callback='parse_item',
                                follow=True
                                )
    rules = (
        rule_product_details,
             )
    def parse_item(self, response):
        yield {
            'Title' : response.xpath('//div[@class="row"]//div[@class="col-xs-12"]//h1[@class="bx-title"]')
        }