import json
import scrapy # type: ignore

from dlscraper.enum import backing, possible, sizes
from dlscraper.items import Diaper


class KitinitiativeSpider(scrapy.Spider):
    name = "kitnitiative"
    allowed_domains = ["kitnitiative.com"]
    start_urls = ["https://kitnitiative.com/products.json"]

    waists = {
        "Medium": {
            "low": 28,
            "high": 44,
        },
        "Large": {
            "low": 32,
            "high": 55,
        },
    }

    def parse(self, response):
        diaper = Diaper()
        diaper['backing'] = backing.PLASTIC
        diaper['brand'] = "Kitnitiative"
        diaper['capacity'] = 6800
        diaper['retailer'] = "Kitnitiative"
        diaper['scented'] = possible.NO
        diaper['tapes'] = 4
        diaper['title'] = "Adventure Puffs!"
        data = json.loads(response.text)
        product = data.get('products', [])[2]
        for variant in product.get('variants', []):
            if variant.get('option1') == "Mixed Size Sample":
                continue
            id = variant.get('id')
            waist = self.waists[variant.get('option1')]
            diaper['id'] = id
            diaper['in_stock'] = possible.YES if variant.get('available') else possible.NO
            diaper['notes'] = []
            # TODO: scrape this
            diaper['on_sale'] = possible.MAYBE
            diaper['price'] = float(variant.get("price"))
            diaper['size'] = variant.get('option1')
            diaper['units'] = int(variant.get('option2'))
            diaper['url'] = f'https://kitnitiative.com/products/adventure-puffs-diapers?variant={id}'
            diaper['waist_low'] = waist.get('low')
            diaper['waist_high'] = waist.get('high')
            yield diaper