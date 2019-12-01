# -*- coding: utf-8 -*-
import scrapy

class HousesSpider(scrapy.Spider):
    name = 'houses'

    def count_floors(self, num, unit):
        if unit in ['trệt', 'lầu', 'tret', 'lau']:
            return num
        if unit == 'lửng' or unit == 'lung':
            return num * 0.5
        return 0

    def handle_floors(self, floors):
        temp = list(map(lambda x: x.strip(), floors.replace('+', ',').split(',')))
        final_floors = 0
        for f in temp:
            if f.isdigit():
                final_floors += float(f)
            else:
                parts = f.split(' ')
                if len(parts) == 1:
                    final_floors += self.count_floors(1, parts[0])
                else:
                    final_floors += self.count_floors(float(parts[0]), parts[1])
        return final_floors

    def start_requests(self):
        request_url = 'https://propzy.vn/mua/ban-nha-rieng-tphcm'
        request_urls = map(lambda i: request_url + '/p' + str(i), range(1, 220))
        for url in request_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        home_items = response.xpath('//div[@itemscope]')
        for home_item in home_items:
            detail_url = home_item.xpath('.//a[@itemprop="url"]/@href').extract_first()
            absolute_detail_url = response.urljoin(detail_url)
            yield scrapy.Request(url=absolute_detail_url, callback=self.home_parse)
    
    def home_parse(self, response):
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
        floors = div_info.xpath('.//span[@class="elements floors"]/text()').get()
        if floors:
            floors = floors.split(':')[1].strip()
            floors = self.handle_floors(floors)
        ledger = div_info.xpath('.//span[@class="elements ledger"]/text()').get()
        if ledger:
            ledger = ledger.split(':')[1].strip()
        bedroom = div_info.xpath('.//span[@class="elements bedroom"]/text()').get()
        if bedroom:
            bedroom = int(bedroom.split(':')[1].strip())
        bathroom = div_info.xpath('.//span[@class="elements bathroom"]/text()').get()
        if bathroom:
            bathroom = int(bathroom.split(':')[1].strip())

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
        #design
        design = div_utilities.xpath('.//span[@data-id="39"]').get()
        is_design = 1 if design else 0
        #security
        security = div_utilities.xpath('.//span[@data-id="40"]').get()
        is_security = 1 if security else 0
        #vehicle park
        vehicle_park = div_utilities.xpath('.//span[@data-id="41"]').get()
        is_vehicle_park = 1 if vehicle_park else 0

        yield {
            'Price': price,
            'Type': 'Nhà',
            'Acreage': acreage,
            'District': district,
            'Ward': ward,
            'Length': length,
            'Width': width,
            'Direction': direction,
            'Alley': alley,
            'Floors': floors,
            'Ledger': ledger,
            'Bedroom': bedroom,
            'Bathroom': bathroom,
            'Is Market': is_market,
            'Is Hospital': is_hospital,
            'Is Park': is_park,
            'Is School': is_school,
            'Is Alley Ventilation': is_alley_ventilation,
            'Is Facade': is_facade,
            'Is Urgent Sale': is_urgent_sale,
            'Is Center': is_center,
            'Is Design': is_design,
            'Is Security': is_security,
            'Is Vehicle Park': is_vehicle_park
        }
