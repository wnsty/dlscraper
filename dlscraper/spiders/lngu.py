import json
import re
import scrapy  # type: ignore

from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes


class LnguSpider(scrapy.Spider):
    name = "lngu"
    allowed_domains = ["lngu-abdl.com"]
    start_urls = ["https://lngu-abdl.com/products.json"]
    units_pattern = re.compile(r"(\d{2}) diapers")
    price_pattern = re.compile(r"\$(\d{2,3}.?\d{0,2})")
    sizes = {
        "M": sizes.MEDIUM,
        "L": sizes.LARGE,
        "XL": sizes.XLARGE,
    }
    discount = {10: 1, 40: 1.66333}
    reference = {
        "LNGU - Dragoonz": {
            "capacity": 9500,
            "backing": backing.PLASTIC,
            "Medium": {
                "low": 27,
                "high": 39,
            },
            "Large": {
                "low": 39,
                "high": 51,
            },
            "XLarge": {
                "low": 40,
                "high": 58,
            },
        },
        "LNGU - Big Ears Baby": {
            "capacity": 7500,
            "backing": backing.CLOTH,
            "Medium": {
                "low": 27,
                "high": 39,
            },
            "Large": {
                "low": 39,
                "high": 51,
            },
            "XLarge": {
                "low": 40,
                "high": 58,
            },
        },
        "LNGU - Candy Fluff": {
            "capacity": 5000,
            "backing": backing.PLASTIC,
            "Medium": {
                "low": 28,
                "high": 44,
            },
            "Large": {
                "low": 31,
                "high": 55,
            },
            "XLarge": {
                "low": 40,
                "high": 58,
            },
        },
    }

    def parse(self, response):
        data = json.loads(response.text)
        for product in data.get("products", []):
            diaper = Diaper()
            title = product.get("title")
            handle = product.get("handle")
            diaper["backing"] = self.reference.get(title).get("backing")
            diaper["brand"] = "LNGU"
            diaper["capacity"] = self.reference.get(title).get("capacity")
            diaper["retailer"] = "LNGU"
            diaper["scented"] = possible.NO
            diaper["tapes"] = 4
            diaper["title"] = title
            print(title)
            for variant in product.get("variants", []):
                id = variant.get("id")
                size = self.sizes.get(variant.get("option1"))
                url = f"https://lngu-abdl.com/products/{handle}?variant={id}"
                waist = self.reference.get(title).get(size)
                diaper["id"] = id
                diaper["in_stock"] = (
                    possible.YES if variant.get("available") == True else possible.NO
                )
                diaper["notes"] = []
                # TODO: scrape this
                diaper["on_sale"] = possible.MAYBE
                diaper["price"] = float(variant.get("price"))
                diaper["size"] = size
                diaper["url"] = url
                diaper["waist_low"] = waist.get("low")
                diaper["waist_high"] = waist.get("high")
                # TODO: fix this
                yield scrapy.Request(
                    url, callback=self.parse_diaper, cb_kwargs=dict(diaper=diaper.copy())
                )

    def parse_diaper(self, response, diaper):
        labels = response.css("label.qty-swatch span::text").getall()
        if labels == []:
            diaper["units"] = 10
            yield diaper
            return
        for label in labels:
            diaper["units"] = int(self.units_pattern.search(label).group(1))
            diaper["price"] = float(self.price_pattern.search(label).group(1))
            yield diaper
