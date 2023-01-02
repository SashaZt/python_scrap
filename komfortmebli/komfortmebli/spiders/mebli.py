import scrapy



class MebliSpider(scrapy.Spider):
    name = 'mebli'
    allowed_domains = ['komfortmebli.com.ua']
    start_urls = ['http://komfortmebli.com.ua/']

    def parse(self, response, **kwargs):
        # catalog Ходим по уровням пока не дойдем до продукта
        href_level_01 = response.xpath('//nav//li[contains(@class,"bx-nav-1-lvl")]/a/@href').extract()
        href_level_02 = response.xpath('//div[@class="bx_catalog_tile"]//li/a/@href').extract()
        href_level_03 = response.xpath('//div[@class="bx_catalog_tile"]//li/a/@href').extract()
        yield from response.follow_all(href_level_01)
        yield from response.follow_all(href_level_02)
        yield from response.follow_all(href_level_03)

        # Product как только находим ссылку входим в нее и передаем дальше в parse_item
        product = response.xpath(
            '//div[@class="col-sm-4 product-item-big-card"]//div[@class="product-item-title"]/a/@href').extract()
        yield from response.follow_all(product, callback=self.parse_item)

        # pagination
        hrefs = response.xpath('//li[@class="bx-pag-next"]/a/@href').extract()

    # Разбираем страницу товара и передаем в item а дальше обезательно в yield item
    def parse_item(self, response, **kwargs):
        title = response.xpath('//div[@class="container-fluid"]//h1/text()').get()
        categ = response.xpath('//div[@class="bx-breadcrumb-item"][last()]/span/text()').extract()

        price_old = response.xpath('//div[@class="product-item-detail-price-old"]/text()').get().replace('\n',
                                                                                                         '').replace(
            '\t', '').replace('\r', '').strip()
        price_new = response.xpath('//div[@class="product-item-detail-price-current"]/text()').get().replace('\n',
                                                                                                             '').strip()
        des = response.xpath('//div[@class="product-item-detail-tab-content active"]//b/text()').getall()
        images = response.xpath('//div[@class="product-item-detail-slider-images-container"]//img/@src').extract()
        nalichie = response.xpath('//*[@id="brand_215422_BrandReference_7_xXGM1R_vidget"]/span/text()').get()


        name_1 = response.xpath('//dt[1]/text()').extract_first().strip()
        value_1 = response.xpath('//dd[1]/text()').extract_first().strip()
        name_2 = response.xpath('//dt[2]/text()').extract_first().strip()
        value_2 = response.xpath('//dd[2]/text()').extract_first().strip()
        name_3 = response.xpath('//dt[3]/text()').extract_first().strip()
        value_3 = response.xpath('//dd[3]/text()').extract_first().strip()
        name_4 = response.xpath('//dt[4]/text()').extract_first().strip()
        value_4 = response.xpath('//dd[4]/text()').extract_first().strip()
        name_5 = response.xpath('//dt[5]/text()').extract_first().strip()
        value_5 = response.xpath('//dd[5]/text()').extract_first().strip()
        name_6 = response.xpath('//dt[6]/text()').extract_first().strip()
        value_6 = response.xpath('//dd[6]/text()').extract_first().strip()
        name_7 = response.xpath('//dt[7]/text()').extract_first().strip()
        value_7 = response.xpath('//dd[7]/text()').extract_first().strip()
        name_8 = response.xpath('//dt[8]/text()').extract_first().strip()
        value_8 = response.xpath('//dd[8]/text()').extract_first().strip()
        name_9 = response.xpath('//dt[9]/text()').extract_first().strip()
        value_9 = response.xpath('//dd[9]/text()').extract_first().strip()
        name_10 = response.xpath('//dt[10]/text()').extract_first().strip()
        value_10 = response.xpath('//dd[10]/text()').extract_first().strip()

        # name_value = dict(zip(name, value))
        # for i in name_value:
        #     print(i[0], i[-1])

        # Удалить символы из каждого итема
        # proper = [item.replace('\n', '') for item in proper]
        # proper = [item.strip() for item in proper]
        item = {
            'title': title,
            'categ': categ,
            'price_old': price_old,
            'price_new': price_new,
            'nalichie':nalichie,
            name_1: value_1,
            name_2: value_2,
            name_3: value_3,
            name_4: value_4,
            name_5: value_5,
            name_6: value_6,
            name_7: value_7,
            name_8: value_8,
            name_9: value_9,
            name_10: value_10,
            'images': images


        }
        yield item
