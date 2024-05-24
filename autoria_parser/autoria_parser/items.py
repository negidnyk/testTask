import scrapy
import datetime

class AutoriaParserItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    region = scrapy.Field()
    mileage = scrapy.Field()
    color = scrapy.Field()
    cabin_color = scrapy.Field()
    cabin_material = scrapy.Field()
    ad_creation_date = scrapy.Field()
    seller_contacts = scrapy.Field()
