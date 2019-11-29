# -*- coding: utf-8 -*-
import scrapy

class LandsSpider(scrapy.Spider):
    name = 'lands'
    
    def start_requests(self):
        request_url = 'https://propzy.vn/mua/ban-dat-nen-tphcm'
        request_urls = map(lambda i: request_url + '/p' + str(i), range(1, 100))
        for url in request_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        land_items = response.xpath('//div[@itemscope]')
        for land_item in land_items:
            detail_url = land_item.xpath('.//a[@itemprop="url"]/@href').extract_first()
            absolute_detail_url = response.urljoin(detail_url)
            yield scrapy.Request(url=absolute_detail_url, callback=self.land_parse)
    
    def land_parse(self, response):
        ##title part
        div_title = response.xpath('//html/body/section/div[1]/div/div[2]/div[1]/div/div[1]/div[3]/div[2]')
        price = div_title.xpath('.//span[@class="span-price"]/text()').get()
        if price:
            temp = price.split(' ')
            num_price = float(temp[0].replace(',', '.'))
            price = num_price * 1000000 if temp[1] == 'tỷ' else num_price * 1000

        acreage = div_title.xpath('.//span[@class="span-acreage"]/text()').get()
        if acreage:
            acreage = float(acreage.replace('m²', '').replace(',', '.'))
        district = div_title.xpath('.//p[contains(@class, "p-district")]/a[1]/span/text()').get()
        ward = div_title.xpath('.//p[contains(@class, "p-district")]/a[2]/span/text()').get()

        ##info part
        div_info = response.xpath('//html/body/section/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/div')
        length = div_info.xpath('.//span[@class="elements length"]/text()').get()
        if length:
            length = float(length.split(':')[1].strip().replace('m', '').replace(',', '.'))
        width = div_info.xpath('.//span[@class="elements width"]/text()').get()
        if width:
            width = float(width.split(':')[1].strip().replace('m', '').replace(',', '.'))
        direction = div_info.xpath('.//span[@class="elements direction"]/text()').get()
        if direction:
            direction = direction.split(':')[1].strip()
        alley = div_info.xpath('.//span[@class="elements alley"]/text()').get()
        if alley:
            alley = float(alley.split(':')[1].strip().replace('m', '').replace(',', '.'))
        ledger = div_info.xpath('.//span[@class="elements ledger"]/text()').get()
        if ledger:
            ledger = ledger.split(':')[1].strip()
        ##utilities part
        div_utilities = response.xpath('//html/body/section/div[1]/div/div[2]/div[1]/div/div[1]/div[5]/div')
        #market
        market = div_utilities.xpath('.//span[@data-id="29"]').get()
        is_market = 1 if market else 0
        #hospital
        hospital = div_utilities.xpath('.//span[@data-id="30"]').get()
        is_hospital = 1 if hospital else 0
        #park
        park = div_utilities.xpath('.//span[@data-id="31"]').get()
        is_park = 1 if park else 0
        #school
        school = div_utilities.xpath('.//span[@data-id="32"]').get()
        is_school = 1 if school else 0
        #alley ventilation
        alley_ventilation = div_utilities.xpath('.//span[@data-id="34"]').get()
        is_alley_ventilation = 1 if alley_ventilation else 0
        #facade
        facade = div_utilities.xpath('.//span[@data-id="36"]').get()
        is_facade = 1 if facade else 0
        #urgent sale
        urgent_sale = div_utilities.xpath('.//span[@data-id="37"]').get()
        is_urgent_sale = 1 if urgent_sale else 0
        #center
        center = div_utilities.xpath('.//span[@data-id="38"]').get()
        is_center = 1 if center else 0
        #security
        security = div_utilities.xpath('.//span[@data-id="40"]').get()
        is_security = 1 if security else 0

        yield {
            'Price': price,
            'Acreage': acreage,
            'District': district,
            'Ward': ward,
            'Length': length,
            'Width': width,
            'Direction': direction,
            'Alley': alley,
            'Ledger': ledger,
            'Is Market': is_market,
            'Is Hospital': is_hospital,
            'Is Park': is_park,
            'Is School': is_school,
            'Is Alley Ventilation': is_alley_ventilation,
            'Is Facade': is_facade,
            'Is Urgent Sale': is_urgent_sale,
            'Is Center': is_center,
            'Is Security': is_security
        }
