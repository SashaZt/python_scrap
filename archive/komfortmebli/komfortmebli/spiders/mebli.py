import scrapy



class MebliSpider(scrapy.Spider):
    name = 'mebli'
    allowed_domains = ['komfortmebli.com.ua']
    start_urls = ['https://komfortmebli.com.ua/ua/']

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

        price_old = response.xpath('//div[@class="product-item-detail-price-old"]/text()').get().replace('\n','').replace('\t', '').replace('\r', '').strip()
        price_new = response.xpath('//div[@class="product-item-detail-price-current"]/text()').get().replace('\n','').strip()
        # des = response.xpath('//div[@class="product-item-detail-tab-content active"]//text()').extract()
        images = response.xpath('//div[@class="product-item-detail-slider-images-container"]//img/@src').extract()
        # nalichie = response.xpath('//*[@id="brand_215422_BrandReference_7_xXGM1R_vidget"]/span/text()').get()

        name_1 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[1]/text()').extract_first().strip()
        if name_1 is not None:
            name_1 = name_1
        value_1 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[1]/text()').extract_first().strip().replace('.', ',')
        if value_1 is not None:
            value_1 = value_1
        name_2 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[2]/text()').extract_first().strip()
        if name_2 is not None:
            name_2 = name_2
        value_2 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[2]/text()').extract_first().strip().replace('.', ',')
        if value_2 is not None:
            value_2 = value_2
        name_3 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[3]/text()').extract_first().strip()
        if name_3 is not None:
            name_3 = name_3
        value_3 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[3]/text()').extract_first().strip().replace('.', ',')
        if value_3 is not None:
            value_3 = value_3
        name_4 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[4]/text()').extract_first().strip()
        if name_4 is not None:
            name_4 = name_4
        value_4 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[4]/text()').extract_first().strip().replace('.', ',')
        if value_4 is not None:
            value_4 = value_4
        name_5 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[5]/text()').extract_first().strip()
        if name_5 is not None:
            name_5 = name_5
        value_5 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[5]/text()').extract_first().strip().replace('.', ',')
        if value_5 is not None:
            value_5 = value_5
        name_6 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[6]/text()').extract_first().strip()
        if name_6 is not None:
            name_6 = name_6
        value_6 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[6]/text()').extract_first().strip().replace('.', ',')
        if value_6 is not None:
            value_6 = value_6
        name_7 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[7]/text()').extract_first().strip()
        if name_7 is not None:
            name_7 = name_7
        value_7 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[7]/text()').extract_first().strip().replace('.', ',')
        if value_7 is not None:
            value_7 = value_7
        name_8 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[8]/text()').extract_first().strip()
        if name_8 is not None:
            name_8 = name_8
        else:
            name_8 = 'No'
        value_8 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[8]/text()').extract_first().strip().replace('.', ',')
        if value_8 is not None:
            value_8 = value_8
        else:
            value_8 = 'No'
        name_9 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[9]/text()').extract_first().strip()
        if name_9 is not None:
            name_9 = name_9
        else:
            name_9 = 'No'
        value_9 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[9]/text()').extract_first().strip().replace('.', ',')
        if value_9 is not None:
            value_9 = value_9
        else:
            value_9 = 'No'
        name_10 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[10]/text()').extract_first().strip()
        if name_10 is not None:
            name_10 = name_10
        else:
            name_10 = 'No'
        value_10 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[10]/text()').extract_first().strip().replace('.', ',')
        if value_10 is not None:
            value_10 = value_10
        else:
            value_10 = 'No'
        name_11 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[11]/text()').extract_first().strip()
        if name_11 is not None:
            name_11 = name_11
        else:
            name_11 = 'No'
        value_11 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[11]/text()').extract_first().strip().replace('.', ',')
        if value_11 is not None:
            value_11 = value_11
        else:
            value_11 = 'No'
        name_12 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[12]/text()').extract_first().strip()
        if name_12 is not None:
            name_12 = name_12
        else:
            name_12 = 'No'
        value_12 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[12]/text()').extract_first().strip().replace('.', ',')
        if value_12 is not None:
            value_12 = value_12
        else:
            value_12 = 'No'
        name_13 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[13]/text()').extract_first().strip()
        if name_13 is not None:
            name_13 = name_13
        else:
            name_13 = 'No'
        value_13 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[13]/text()').extract_first().strip().replace('.', ',')
        if value_13 is not None:
            value_13 = value_13
        else:
            value_13 = 'No'
        name_14 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[14]/text()').extract_first().strip()
        if name_14 is not None:
            name_14 = name_14
        else:
            name_14 = 'No'
        value_14 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[14]/text()').extract_first().strip().replace('.', ',')
        if value_14 is not None:
            value_14 = value_14
        else:
            value_14 = 'No'
        name_15 = response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dt[15]/text()').extract_first().strip()
        if name_15 is not None:
            name_15 = name_15
        else:
            name_15 = 'No'
        value_15 =response.xpath('//div[@class="col-sm-8 col-md-9"]//div//dl/dd[15]/text()').extract_first().strip().replace('.', ',')
        if value_15 is not None:
            value_15 = value_15
        else:
            value_15 = 'No'
        # except:
        #     name_1 = 'No name_1'
        #     value_1 = 'No value_1'
        #     name_2 = 'No name_1'
        #     value_2 = 'No value_1'
        #     name_3 = 'No name_1'
        #     value_3 = 'No value_1'
        #     name_4 = 'No name_1'
        #     value_4 = 'No value_1'
        #     name_5 = 'No name_1'
        #     value_5 = 'No value_1'
        #     name_6 = 'No name_1'
        #     value_6 = 'No value_1'
        #     name_7 = 'No name_1'
        #     value_7 = 'No value_1'
        #     name_9 = 'No name_1'
        #     value_9 = 'No value_1'
        #     name_10 = 'No name_1'
        #     value_10 = 'No value_1'
        #     name_11 = 'No name_1'
        #     value_11 = 'No value_1'
        #     name_12 = 'No name_1'
        #     value_12 = 'No value_1'
        #     name_13 = 'No name_1'
        #     value_13 = 'No value_1'
        #     name_14 = 'No name_1'
        #     value_14 = 'No value_1'
        #     name_15 = 'No name_1'
        #     value_15 = 'No value_1'
        #     name_8 = 'No name_1'
        #     value_8 = 'No value_1'

        item = {
            'title': title,
            'categ': categ,
            'price_old': price_old,
            'price_new': price_new,
            name_1: value_1,
            name_2: value_2,
            name_3: value_3,
            name_4: value_4,
            name_5: value_5,
            name_6: value_6,
            name_7: value_7,
            # name_8: value_8,
            # name_9: value_9,
            # name_10: value_10,
            # name_11: value_11,
            # name_12: value_12,
            # name_13: value_13,
            # name_14: value_14,
            # name_15: value_15,
            'images': images



        }
        yield item
