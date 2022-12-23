from playwright.sync_api import Playwright, sync_playwright, expect
import scrapy

from scrapy_playwright.page import PageMethod
from playwright.async_api import async_playwright
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exporters import CsvItemExporter

class DoctorSpider(scrapy.Spider):
    name = 'doctor'


    start_urls = ["https://www.znanylekarz.pl/szukaj?q=&loc=Warszawa"]


    def parse(self, response):

        for link in response.xpath('//div[@class="media-body"]/h3/a/@href').extract():
            yield response.follow(link, meta={'playwright': True}, dont_filter=True, callback=self.parse_avto_tovar)
        for i in range(1, 2):
            next_page = f"https://www.znanylekarz.pl/szukaj?q=&loc=Warszawa&page={i}"
            yield response.follow(next_page, callback=self.parse)

    async def parse_avto_tovar(self, response):
        yield {
            'name': response.xpath('//div[@data-id="profile-fullname-wrapper"]/text()').get(),
            # 'sku_product': response.xpath('//dd[@data-product-sku=""]/text()').get(),
            # 'group_products': response.xpath('//a[@class="breadcrumb-label"]/text()')[1].get(),
            # 'price_products': response.xpath('//span[@class="price price--withoutTax"]/text()')[0].get(),
            # 'img_product': response.xpath('//figure[@data-fancybox="gallery"]/@href').get()

        }





































# class DoctorSpider(scrapy.Spider):
#     name = 'doctor'
#
#
#     start_urls = ["https://www.znanylekarz.pl/szukaj?q=&loc=Warszawa"]
#
#
#     def parse(self, response):
#
#         for link in response.xpath('//div[@class="media-body"]/h3/a/@href').extract():
#             yield response.follow(link, meta={'playwright': True}, dont_filter=True, callback=self.parse_avto_tovar)
#         for i in range(1, 2):
#             next_page = f"https://www.znanylekarz.pl/szukaj?q=&loc=Warszawa&page={i}"
#             yield response.follow(next_page, callback=self.parse)
#
#     async def parse_avto_tovar(self, response):
#         yield {
#             'name': response.xpath('//div[@data-id="profile-fullname-wrapper"]/text()').get(),
#             # 'sku_product': response.xpath('//dd[@data-product-sku=""]/text()').get(),
#             # 'group_products': response.xpath('//a[@class="breadcrumb-label"]/text()')[1].get(),
#             # 'price_products': response.xpath('//span[@class="price price--withoutTax"]/text()')[0].get(),
#             # 'img_product': response.xpath('//figure[@data-fancybox="gallery"]/@href').get()
#
#         }




    #
    # def start_requests(self):
    #     yield scrapy.Request('https://www.znanylekarz.pl/szukaj?q=&loc=Warszawa',
    #                          meta=dict(
    #                              playwright=True,
    #                              playwright_include_page=True,
    #                              playwright_page_methods=[
    #                                  PageMethod('wait_for_selector', 'div#onetrust-button-group')
    #                              ]
    #                          )
    #                          )
    #
    # async def parse(self, response):
    #     for i in response.xpath('//div[@class="catalog-product-m-item"]'):
    #         yield {
    #             'title': i.xpath('//div[@class="product-d"]/a/text()').get(),
    #             'prise': i.xpath('//span[@class="change-prise"]/text()').get()
    #         }