import scrapy


class KormSpider(scrapy.Spider):
    name = 'korm'
    allowed_domains = ['e-zoo.com.ua']
    start_urls = ['https://e-zoo.com.ua/ua/prices-drop']

    def parse(self, response, **kwargs):
        # catalog Ходим по уровням пока не дойдем до продукта
        href_product = response.xpath('//div[@class="product-d"]/a/@href').extract()
        # href_level_02 = response.xpath('//div[@class="bx_catalog_tile"]//li/a/@href').extract()
        # href_level_03 = response.xpath('//div[@class="bx_catalog_tile"]//li/a/@href').extract()


        #Ходим по пагинации
        href_pagan = response.xpath('//ul[@class="pagination"]//a/@href').extract()
        yield from response.follow_all(href_pagan)

        # Заходим в карточку продукта
        yield from response.follow_all(href_product, callback=self.parse_item)
        # yield from response.follow_all(href_level_02)
        # yield from response.follow_all(href_level_03)
        #
        # # Product как только находим ссылку входим в нее и передаем дальше в parse_item
        # product = response.xpath(
        #     '//div[@class="col-sm-4 product-item-big-card"]//div[@class="product-item-title"]/a/@href').extract()
        # yield from response.follow_all(product, callback=self.parse_item)
        #
        # # pagination
        # hrefs = response.xpath('//li[@class="bx-pag-next"]/a/@href').extract()

    # Разбираем страницу товара и передаем в item а дальше обезательно в yield item
    def parse_item(self, response, **kwargs):

        title = response.xpath('//div[@class="d-none d-lg-flex flex-column position-relative"]//h1[@class="h2"]/text()').get()
        price = response.xpath('//div[@class="product-food-prise d-flex flex-column"]//span[@class="relevant-prise"]/text()').get()
        price_all = response.xpath('//div[@class="mb-20 product-food-weight-b"]//span//label//text()').get()
        country = response.xpath('//div[@class="product-food-components active"]/text()').get()
        table_td_01 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[1]/td[1]/text()').get().strip()
        table_tr_01 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[1]/td[2]/text()').get().strip()
        table_td_02 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[2]/td[1]/text()').get().strip()
        table_tr_02 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[2]/td[2]/text()').get().strip()
        table_td_03 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[3]/td[1]/text()').get().strip()
        table_tr_03 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[3]/td[2]/text()').get().strip()
        table_td_04 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[4]/td[1]/text()').get().strip()
        table_tr_04 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[4]/td[2]/text()').get().strip()
        table_td_05 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[5]/td[1]/text()').get().strip()
        table_tr_05 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[5]/td[2]/text()').get().strip()
        table_td_06 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[6]/td[1]/text()').get().strip()
        table_tr_06 = response.xpath('//div[@class="tab-content"]//div[@class="table-responsive prod-options-tbl"]//table[@class="table"]//tbody/tr[6]/td[2]/text()').get().strip()
        descrip_01 = response.xpath('//div[@id="prod_desc_cont"]//p[1]/text()').get()
        descrip_02 = response.xpath('//div[@id="prod_desc_cont"]//p[2]/text()').get()
        img = response.xpath('//div[@class="swiper-product"]//img/@src').get

        # price_old = response.xpath('//div[@class="product-item-detail-price-old"]/text()').get().replace('\n',
        #                                                                                                  '').replace(
        #     '\t', '').replace('\r', '').strip()
        # price_new = response.xpath('//div[@class="product-item-detail-price-current"]/text()').get().replace('\n',
        #                                                                                                      '').strip()
        # des = response.xpath('//div[@class="product-item-detail-tab-content active"]//b/text()').getall()
        # proper = response.xpath(
        #     '//div[@class="product-item-detail-tab-content"]//dl[@class="product-item-detail-properties"]//dt/text()').extract()
        # proper_01_all = []
        # for i in proper:
        #     proper_01_all.append(i.strip().replace('\n', ''))
        # proper_02 = response.xpath(
        #     '//div[@class="product-item-detail-tab-content"]//dl[@class="product-item-detail-properties"]//dd/text()').extract()
        # proper_02_all = []
        # for j in proper_02:
        #     proper_02_all.append(j.strip().replace('\n', ''))
        #
        # # Удалить символы из каждого итема
        # # proper = [item.replace('\n', '') for item in proper]
        # # proper = [item.strip() for item in proper]
        item = {
            'title': title,
            'price': price,
            'country': country,
            table_td_01 : table_tr_01,
            table_td_02 : table_tr_02,
            table_td_03 : table_tr_03,
            table_td_04 : table_tr_04,
            table_td_05 : table_tr_05,
            table_td_06 : table_tr_06,
            'descrip_01' : descrip_01,
            'descrip_02' : descrip_02




        }
        yield item
