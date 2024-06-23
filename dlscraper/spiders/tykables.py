import json
import re
import scrapy # type: ignore

from dlscraper.enum import backing, possible, sizes
from dlscraper.items import Diaper


class TykablesSpider(scrapy.Spider):
    name = "tykables"
    allowed_domains = ["tykables.com"]
    start_urls = ["https://tykables.com/products.json?limit=1000"]
    sizes_reference = {
        "Medium": sizes.MEDIUM,
        "Large": sizes.LARGE,
        "XL": sizes.XLARGE,
    }
    units_pattern = re.compile(r'\d{1,2}')
    capacity_pattern = re.compile(r"(\d{4})ml")
    size_pattern = re.compile(r"(Medium)|(Large)|(XL)")
    waist_pattern = re.compile(r'(\d{2})"- ?(\d{2})"')

    def parse(self, response):
        data = json.loads(response.text)

        for product in data.get("products", []):
            if product.get("product_type") != "Adult Diapers":
                continue
            if product.get("vendor") == "Mix & Match":
                continue
            if "Dubbler" in product.get("tags", []):
                continue
            handle = product.get('handle')
            diaper = Diaper()
            diaper["backing"] = backing.PLASTIC
            diaper["brand"] = brand(product.get("title"))
            diaper["capacity"] = int(
                self.capacity_pattern.search(product.get("body_html")).group(1)
            )
            diaper["retailer"] = "Tykables"
            diaper["scented"] = possible.NO
            diaper["tapes"] = 4
            diaper["title"] = product.get("title")
            
            for variant in product.get("variants", []):
                id = variant.get("id")
                waist_match = self.waist_pattern.search(variant.get('option1'))
                waist = {
                    "low": waist_match.group(1),
                    "high": waist_match.group(2),
                }
                diaper["id"] = id
                diaper['in_stock'] = possible.YES if variant.get('available') else possible.NO
                diaper['notes'] = []
                # TODO: scrape this
                diaper['on_sale'] = possible.MAYBE
                diaper['price'] = float(variant.get('price'))
                diaper['units'] = int(self.units_pattern.search(variant.get('option2')).group(0))
                diaper["size"] = self.sizes_reference.get(
                    self.size_pattern.search(variant.get("option1")).group(0)
                )
                diaper['url'] = f'https://tykables.com/products/{handle}?variant={id}'
                diaper['waist_low'] = waist.get('low')
                diaper['waist_high'] = waist.get('high')
                yield diaper

def brand(title: str):
    if title.startswith("Str8up"):
        return "NRU"
    return "Tykables"