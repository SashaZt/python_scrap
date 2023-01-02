import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exporters import CsvItemExporter


class BookSpider(scrapy.Spider):
    name = 'avto_parts'
    start_urls = ["https://shop.moderngroup.com/fleetguard/"]

    def parse(self, response):
        for link in response.xpath('//h4[@class="card-title"]/a/@href').extract():
            yield response.follow(link, dont_filter=True, callback=self.parse_avto_tovar)
        for i in range(1, 2):
            next_page = f"https://shop.moderngroup.com/fleetguard/?sort=bestselling&page={i}"
            yield response.follow(next_page, callback=self.parse)

    def parse_avto_tovar(self, response):
        yield {
            'name': response.xpath('//h1[@class="productView-title"]/text()').get(),
            'sku_product': response.xpath('//dd[@data-product-sku=""]/text()').get(),
            'group_products': response.xpath('//a[@class="breadcrumb-label"]/text()')[1].get(),
            'price_products': response.xpath('//span[@class="price price--withoutTax"]/text()')[0].get(),
            'img_product': response.xpath('//figure[@data-fancybox="gallery"]/@href').get()

        }