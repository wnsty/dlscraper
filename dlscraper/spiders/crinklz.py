import json
import scrapy # type: ignore

from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes

class CrinklzSpider(scrapy.Spider):
    name = "crinklz"
    allowed_domains = ["www.crinklz.com"]
    start_urls = ["https://www.crinklz.com/products.json"]
    sizes = {
        "Small": sizes.SMALL,
        "Medium": sizes.MEDIUM,
        "Large": sizes.LARGE,
        "X-Large": sizes.XLARGE,
    }
    waists = {
        "Small": {
            "low": 21,
            "high": 31,
        },
        "Medium": {
            "low": 29,
            "high": 43,
        },
        "Large": {
            "low": 43,
            "high": 59,
        },
        "XLarge": {
            "low": 51,
            "high": 69,
        },
    }

    def parse(self, response):
        data = json.loads(response.text)
        for product in data.get('products', []):
            if product.get('product_type') != 'Diapers':
                continue
            diaper = Diaper()
            title = product.get('title')
            handle = product.get('handle')
            diaper['backing'] = backing.PLASTIC
            diaper['brand'] = 'BetterDry' if 'BetterDry' in title else 'Crinklz'
            diaper['capacity'] = 1120
            diaper['notes'] = ['advertised capacity is low']
            # TODO: scrape this
            diaper['on_sale'] = possible.MAYBE
            diaper['retailer'] = 'Crinklz'
            diaper['scented'] = possible.NO
            diaper['tapes'] = 4
            diaper['title'] = title
            for variant in product.get('variants', []):
                id = variant.get('id')
                size = self.sizes.get(variant.get('option1'))
                waist = self.waists.get(size)
                diaper['id'] = id
                diaper['in_stock'] = possible.YES if variant.get("available") else possible.NO
                diaper['price'] = float(variant.get('price'))
                diaper['size'] = size
                diaper['units'] = 60
                diaper['url'] = f'https://www.crinklz.com/en-us/products/{handle}?variant={id}'
                diaper['waist_low'] = waist.get('low')
                diaper['waist_high'] = waist.get('high')
                yield diaper
