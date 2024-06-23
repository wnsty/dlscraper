# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field # type: ignore


class Diaper(Item):
    backing = Field()
    brand = Field()
    capacity = Field()
    id = Field()
    in_stock = Field()
    ml_per_unit_price = Field()
    notes = Field()
    on_sale = Field()
    price = Field()
    retailer = Field()
    scented = Field()
    score = Field()
    size = Field()
    tapes = Field()
    title = Field()
    unit_price = Field()
    units = Field()
    url = Field()
    waist_low = Field()
    waist_high = Field()

class Booster(Item):
    brand = Field()
    capacity = Field()
    id = Field()
    in_stock = Field()
    ml_per_unit_price = Field()
    notes = Field()
    on_sale = Field()
    price = Field()
    retailer = Field()
    scented = Field()
    score = Field()
    title = Field()
    unit_price = Field()
    units = Field()
    url = Field()