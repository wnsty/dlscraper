import json
import re
import scrapy # type: ignore

from dlscraper.enum import backing, possible, sizes
from dlscraper.items import Diaper


class CuddleCooperativeSpider(scrapy.Spider):
    name = "cuddle_cooperative"
    allowed_domains = ["www.thecuddlecooperative.com"]
    start_urls = ["https://www.thecuddlecooperative.com/products.json"]
    units_pattern = re.compile(r'\d{2}')
    size_pattern = re.compile(r'(Medium)|(Large)')
    waists = {
        "Medium": {
            "low": 32,
            "high": 40,
        },
        "Large": {
            "low": 36,
            "high": 50,
        },
    }

    def parse(self, response):
        data = json.loads(response.text)
        for product in data.get('products', []):
            variant = product.get('variants')[0]
            size = self.size_pattern.search(product.get('title')).group(0)
            print(size)
            waist = self.waists.get(size)
            handle = product.get('handle')

            diaper = Diaper()
            diaper['backing'] = backing.PLASTIC
            diaper['brand'] = 'The Cuddle Cooperative'
            diaper['capacity'] = 5000
            diaper['id'] = product.get('id')
            diaper['retailer'] = 'The Cuddle Cooperative'
            diaper['scented'] = possible.NO
            diaper['tapes'] = 4
            diaper['title'] = "Fairyland"
            diaper['in_stock'] = possible.YES if variant.get('available') else possible.NO
            diaper['notes'] = []
            # TODO: scrape this
            diaper['on_sale'] = possible.MAYBE
            diaper['price'] = float(variant.get("price"))
            diaper['size'] = size
            diaper['units'] = int(self.units_pattern.search(product.get('title')).group(0))
            diaper['url'] = f'https://www.thecuddlecooperative.com/products/{handle}'
            diaper['waist_low'] = waist.get('low')
            diaper['waist_high'] = waist.get('high')
            yield diaper
            

