import json
import re
import scrapy # type: ignore

from dlscraper.enum import backing, possible, sizes
from dlscraper.items import Diaper


class PretendAgainSpider(scrapy.Spider):
    name = "pretend_again"
    allowed_domains = ["www.pretendagain.com"]
    start_urls = ["https://www.pretendagain.com/products.json?limit=250"]
    size_reference = {
        "Medium": sizes.MEDIUM,
        "Large": sizes.LARGE,
        "X-Large": sizes.XLARGE,
    }
    waists = {
        "Medium": {
            "low": 28,
            "high": 36,
        },
        "Large": {
            "low": 36,
            "high": 48,
        },
        "X-Large": {
            "low": 48,
            "high": 56,
        },
    }
    units_pattern = re.compile(r'\d{2}')

    def parse(self, response):
        data = json.loads(response.text)
        # TODO: do better...
        product = data.get('products', [])[10]
        diaper = Diaper()
        diaper['backing'] = backing.PLASTIC
        diaper['brand'] = 'TryAgains'
        diaper['capacity'] = 6800
        diaper['retailer'] = 'PretendAgain'
        diaper['scented'] = possible.NO
        diaper['tapes'] = 4
        diaper['title'] = product.get('title')

        for variant in product.get('variants'):
            id = variant.get('id')
            waist = self.waists[variant.get('option1')]
            diaper['id'] = id
            diaper['in_stock'] = possible.YES if variant.get('available') else possible.NO
            diaper['notes'] = []
            # TODO: scrape this
            diaper['on_sale'] = possible.MAYBE
            diaper['price'] = float(variant.get("price"))
            diaper['size'] = self.size_reference.get(variant.get('option1'))
            diaper['units'] = int(self.units_pattern.search(variant.get('option2')).group(0))
            diaper['url'] = f'https://www.pretendagain.com/products/tryagains-diapers?variant={id}'
            diaper['waist_low'] = waist.get('low')
            diaper['waist_high'] = waist.get('high')
            yield diaper