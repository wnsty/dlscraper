import json
import re
import scrapy # type: ignore

from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes

class CutieplusuSpider(scrapy.Spider):
    name = "cutieplusu"
    allowed_domains = ["cutieplusu.com"]
    start_urls = ["https://cutieplusu.com/products.json?limit=1000"]
    sizes = {
        "Size M": sizes.MEDIUM,
        "size M": sizes.MEDIUM,
        "M": sizes.MEDIUM,
        "Size L": sizes.LARGE,
        "size L": sizes.LARGE,
        "L": sizes.LARGE,
    }
    waists = {
        "Medium": {
            "low": 28,
            "high": 38,
        },
        "Large": {
            "low": 36,
            "high": 46,
        },
    }
    units = {
        "1 Pack": 10,
        "1 pack": 10,
        "2 Pack": 20,
        "2 pack": 20,
    }
    units_pattern = re.compile(r'\d')
    double_pattern = re.compile(r'\+')

    def parse(self, response):
        data = json.loads(response.text)
        for product in data.get('products', []):
            title = product.get('title')
            if not 'Diaper' in title or 'Cloth' in title:
                continue
            handle = product.get('handle')
            diaper = Diaper()
            diaper['backing'] = backing.PLASTIC
            diaper['brand'] = 'Cutie Plus U'
            diaper['capacity'] = 5150
            diaper['notes'] = ['derived capacity from oz']
            # TODO: scrape this
            diaper['on_sale'] = possible.MAYBE
            diaper['retailer'] = 'Cutie Plus U'
            diaper['scented'] = possible.NO
            diaper['tapes'] = 4
            diaper['title'] = title
            units_match = self.units_pattern.search(title)
            for variant in product.get('variants', []):
                id = variant.get('id')
                size = self.sizes.get(variant.get('option1'))
                waist = self.waists.get(size)
                diaper['id'] = id
                diaper['in_stock'] = possible.YES if variant.get("available") else possible.NO
                diaper['price'] = float(variant.get('price'))
                diaper['size'] = size
                diaper['url'] = f'https://cutieplusu.com/products/{handle}?variant={id}'
                diaper['waist_low'] = waist.get('low')
                diaper['waist_high'] = waist.get('high')
                print(units_match, self.double_pattern.search(title))
                if units_match is None:
                    if self.double_pattern.search(title) is None:
                        diaper['units'] = self.units.get(variant.get('option2'))
                    else:
                        diaper['units'] = 20
                else:
                    diaper['units'] = int(units_match.group(0))
                yield diaper
