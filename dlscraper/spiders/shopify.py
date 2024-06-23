import scrapy # type: ignore
import json

from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes


class ShopifySpider(scrapy.Spider):
    name = "shopify"

    def parse(self, response):
        data = json.loads(response.text)

        for product in data.get("products", []):
            handle = product.get("handle")
            if self.is_valid(product):
                diaper = Diaper()
                diaper["backing"] = self.backing(product)
                diaper["brand"] = self.brand(product)
                diaper["retailer"] = self.retailer(product)
                diaper["tapes"] = self.tapes(product)
                diaper["title"] = self.title(product)
                for variant in product.get("variants", []):
                    id = variant.get("id")
                    price = float(variant.get("price"))
                    url = self.product_url(handle, variant)
                    diaper_variant = diaper.copy()
                    diaper_variant["id"] = id
                    diaper_variant["in_stock"] = self.in_stock(variant)
                    diaper_variant["price"] = price
                    diaper_variant["scented"] = self.scented(variant)
                    diaper_variant["size"] = self.size(variant)
                    diaper_variant["units"] = self.units(variant)
                    diaper_variant["url"] = url
                    yield scrapy.Request(
                        url,
                        callback=self.parse_diaper,
                        cb_kwargs=dict(diaper_variant=diaper_variant, variant=variant),
                    )

    def parse_diaper(self, response, diaper_variant, variant):
        capacity = self.capacity(response, variant, diaper_variant)
        price = diaper_variant.get("price")
        units = diaper_variant.get("units")
        unit_price = price / units
        ml_per_unit_price = capacity / unit_price
        score = ml_per_unit_price / unit_price
        waist = self.waist(diaper_variant, variant)
        diaper = Diaper()
        diaper["backing"] = diaper_variant.get("backing")
        diaper["brand"] = diaper_variant.get("brand")
        diaper["capacity"] = capacity
        diaper["id"] = diaper_variant.get("id")
        diaper["in_stock"] = diaper_variant.get("in_stock")
        diaper["ml_per_unit_price"] = ml_per_unit_price
        diaper["notes"] = []
        diaper["on_sale"] = self.on_sale(response)
        diaper["price"] = price
        diaper["retailer"] = diaper_variant.get("retailer")
        diaper["scented"] = diaper_variant.get("scented")
        diaper["score"] = score
        diaper["size"] = diaper_variant.get("size")
        diaper["tapes"] = diaper_variant.get("tapes")
        diaper["title"] = diaper_variant.get("title")
        diaper["unit_price"] = unit_price
        diaper["units"] = units
        diaper["url"] = diaper_variant.get("url")
        diaper["waist_low"] = waist.get("low")
        diaper["waist_high"] = waist.get("high")
        for p in self.finalize(diaper):
            yield p

    def backing(self, product):
        return backing.PLASTIC

    def brand(self, product):
        return "Shopify"

    def capacity(self, response, variant, diaper_variant):
        return 1

    def check_tags(self, tags, f):
        for tag in tags:
            if f(tag):
                return True
        return False

    def finalize(self, variant):
        yield variant

    def in_stock(self, variant):
        available = variant.get("available")
        if available is None:
            return possible.MAYBE
        if available:
            return possible.YES
        else:
            return possible.NO

    def is_valid(self, product):
        return True

    def map_tags(self, tags, yes, no, f):
        if self.check_tags(tags, f):
            return yes
        else:
            return no

    def on_sale(self, response):
        return possible.MAYBE

    def product_url(self, handle, variant):
        return self.base_product_url + handle + "?variant=" + str(variant['id'])

    def retailer(self, product):
        return "Shopify"

    def scented(self, variant):
        return possible.MAYBE

    def size(self, variant):
        return sizes.UNKOWN

    def tapes(self, product):
        return 4

    def title(self, product):
        return "Shopify Product"

    def units(self, variant):
        return 1

    def waist(self, diaper_variant, variant):
        return {
            "low": 0,
            "high": 0,
        }
