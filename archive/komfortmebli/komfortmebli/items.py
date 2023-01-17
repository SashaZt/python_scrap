# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    title = scrapy.Field()
    price_old = scrapy.Field()
    price_new = scrapy.Field()
    des = scrapy.Field()
    images = scrapy.Field()

