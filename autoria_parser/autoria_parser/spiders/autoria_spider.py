import scrapy
import re
from datetime import datetime


class CarsSpider(scrapy.Spider):
    name = "cars"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/legkovie/?page=1"]
    pages_count = 10

    def start_requests(self):
        for page in range(0, self.pages_count):
            url = f'https://auto.ria.com/uk/legkovie/?page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.xpath('//div[@class="item ticket-title"]/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_single_car_item)


    async def parse_single_car_item(self, response, **kwargs):

        car_brand_model_year = response.xpath('//span[@class="argument d-link__name"]/text()').get()
        parts = car_brand_model_year.split(' ')
        # Соединим элементы списка, которые относятся к марке и модели, исключая последний элемент (год)
        brand = parts[0]
        model = ' '.join(parts[1:-1])
        year = parts[-1]

        date_pattern = r'\d{2}\.\d{2}\.\d{4}'
        car_item_raw_date_with_text = response.xpath('//span[@class="label mt-15 size13"]/text()').get()
        car_item_date_without_text = re.findall(date_pattern, car_item_raw_date_with_text)
        car_item_date_str = car_item_date_without_text[0]
        car_item_formatted_date = datetime.strptime(car_item_date_str, '%d.%m.%Y').date()

        car_item = {'url': response.request.url,
                    'title': response.xpath('//h1[@class="head"]/@title').get(),
                    'price_in_eur': response.xpath('//span[@class="i-block"]/span[@data-currency="EUR"]/text()').extract()[0],
                    'brand': brand,'model': model,'year': year,
                    'region': response.xpath('//*[@id="breadcrumbs"]/div[3]/a/span/text()').get().strip(),
                    'mileage': response.xpath('//span[@class="size18"]/text()').get(),
                    'color': response.xpath('//span[@class="car-color"]/following-sibling::text()')[0].get().strip(),
                    'cabin_color': response.xpath('//*[@id="details"]/dl/dd[15]/span[2]/text()').get(),
                    'cabin_material': response.xpath('//*[@id="details"]/dl/dd[14]/span[2]/text()').get(),
                    'ad_creation_date': car_item_formatted_date,
                    'seller_contacts': response.xpath('//*[@id="phonesBlock"]/div/span/span[@class="mhide"]/text()').get()
                    }
        yield car_item
