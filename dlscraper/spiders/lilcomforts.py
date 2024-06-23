import json
import scrapy # type: ignore

from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes

class LilcomfortsSpider(scrapy.Spider):
    name = "lilcomforts"
    allowed_domains = ["lilcomforts.com"]
    start_urls = ["https://lilcomforts.com/products.json"]
    sizes = {
        "M": sizes.MEDIUM,
        "L": sizes.LARGE,
        "XL": sizes.XLARGE,
    }
    units = {
        "2 Sample": 2,
        "10 Pack": 10,
        "40 Case": 40,
    }
    waists = {
        "Medium": {
            "low": 28,
            "high": 40,
        },
        "Large": {
            "low": 28,
            "high": 40,
        },
        "XLarge": {
            "low": 28,
            "high": 40,
        },
    }

    def parse(self, response):
        data = json.loads(response.text)
        product = data.get('products')[16]
        diaper = Diaper()
        diaper['backing'] = backing.CLOTH
        diaper['brand'] = 'Lil Comforts'
        diaper['capacity'] = 6500
        diaper['retailer'] = 'Lil Comforts'
        diaper['scented'] = possible.NO
        diaper['title'] = product.get('title')
        for variant in product.get('variants', []):
            id = variant.get('id')
            size = self.sizes.get(variant.get('option1'))
            waist = self.waists.get(size)
            diaper['id'] = id
            diaper['in_stock'] = (
                possible.YES if variant.get("available") == True else possible.NO
            )
            diaper['notes'] = []
            # TODO: scrape this
            diaper['on_sale'] = possible.MAYBE
            diaper['price'] = float(variant.get('price'))
            diaper['size'] = size
            diaper['tapes'] = 4
            diaper['units'] = self.units.get(variant.get('option2'))
            diaper['url'] = f'https://lilcomforts.com/products/cozy-cubs-adult-diapers?variant={id}'
            diaper['waist_low'] = waist.get('low')
            diaper['waist_high'] = waist.get('high')
            yield diaper
