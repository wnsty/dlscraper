import json
import scrapy # type: ignore

from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes

class AbenaSpider(scrapy.Spider):
    name = "abena"
    allowed_domains = ["abenausa.com"]
    start_urls = ["https://abenausa.com/products.json?limit=1000"]
    sizes = {
        "XS": sizes.XSMALL,
        "S": sizes.SMALL,
        "M": sizes.MEDIUM,
        "M4": sizes.MEDIUM,
        "M-L": sizes.MEDIUM,
        "L": sizes.LARGE,
        "L4": sizes.LARGE,
        "L-XL": sizes.LARGE,
        "XL": sizes.XLARGE,
    }
    reference = {
        "Abena Slip": {
            "XS2": {
                "capacity": 1400,
                "Bag": 32,
                "Case": 128,
                "waist": [20, 24],
            },
            "S2": {
                "capacity": 1800,
                "Bag": 28,
                "Case": 84,
                "waist": [24, 33],
            },
            "S4": {
                "capacity": 2200,
                "Bag": 25,
                "Case": 75,
                "waist": [24, 33],
            },
            "M0": {
                "capacity": 1500,
                "Bag": 27,
                "Case": 108,
                "waist": [24, 33],
            },
            "M1": {
                "capacity": 2000,
                "Bag": 26,
                "Case": 104,
                "waist": [28, 43],
            },
            "M2": {
                "capacity": 2600,
                "Bag": 24,
                "Case": 96,
                "waist": [28, 43],
            },
            "M3": {
                "capacity": 3100,
                "Bag": 23,
                "Case": 92,
                "waist": [28, 43],
            },
            "M4": {
                "capacity": 3600,
                "Bag": 21,
                "Case": 84,
                "waist": [28, 43],
            },
            "L0": {
                "capacity": 2000,
                "Bag": 26,
                "Case": 104,
                "waist": [39, 59],
            },
            "L1": {
                "capacity": 2500,
                "Bag": 26,
                "Case": 104,
                "waist": [39, 59],
            },
            "L2": {
                "capacity": 3100,
                "Bag": 22,
                "Case": 88,
                "waist": [39, 59],
            },
            "L3": {
                "capacity": 3400,
                "Bag": 20,
                "Case": 80,
                "waist": [39, 59],
            },
            "L4": {
                "capacity": 4000,
                "Bag": 18,
                "Case": 72,
                "waist": [39, 59],
            },
            "XL2": {
                "capacity": 3400,
                "Bag": 21,
                "Case": 84,
                "waist": [43, 67],
            },
            "XL4": {
                "capacity": 4000,
                "Bag": 12,
                "Case": 48,
                "waist": [43, 67],
            },
        },
        "Abena Slip Flexi-Fit": {
            "M-L1": {
                "waist": [28, 47],
                "capacity": 1800,
                "Bag": 27,
                "Case": 108,
            },
            "L-XL1": {
                "waist": [43, 67],
                "capacity": 2300,
                "Bag": 25,
                "Case": 100,
            },
            "M-L2": {
                "waist": [28, 47],
                "capacity": 2400,
                "Bag": 25,
                "Case": 100,
            },
            "L-XL2": {
                "waist": [43, 67],
                "capacity": 2900,
                "Bag": 22,
                "Case": 88,
            },
            "M-L3": {
                "waist": [28, 47],
                "capacity": 3000,
                "Bag": 23,
                "Case": 92,
            },
            "L-XL3": {
                "waist": [43, 67],
                "capacity": 3200,
                "Bag": 20,
                "Case": 80,
            },
            "M-L4": {
                "waist": [28, 47],
                "capacity": 3400,
                "Bag": 21,
                "Case": 84,
            },
            "L-XL4": {
                "waist": [43, 67],
                "capacity": 3800,
                "Bag": 18,
                "Case": 72,
            },
        },
        "Abena Slip Special": {
            "M4": {
                "waist": [28, 44],
                "capacity": 3600,
                "Bag": 14,
                "Case": 56,
            },
            "L4": {
                "waist": [40, 59],
                "capacity": 4000,
                "Bag": 12,
                "Case": 48,
            },
        },
        "Abri-Form Comfort": {
            "M4": {
                "waist": [28, 44],
                "capacity": 3600,
                "Bag": 14,
                "Case": 42,
            },
            "L4": {
                "waist": [40, 60],
                "capacity": 4000,
                "Bag": 12,
                "Case": 36,
            },
        },
    }

    def parse(self, response):
        data = json.loads(response.text)
        for product in data.get('products', []):
            if not product.get('product_type', '') in ['ABRI FORM COMFORT', 'SLIP FLEXI-FIT', 'SLIP', 'SLIP SPECIAL']:
                continue
            # pretty sure this means it's no longer sold
            if 'b2b' in product.get('tags', []):
                continue
            title = product.get('title')
            # TODO: include these...
            if title == 'Abena Slip Flexi-Fit' or title == 'Abena Slip Special':
                continue
            handle = product.get('handle')
            reference = self.reference.get(title)
            diaper = Diaper()
            # TODO: figure this out
            diaper['backing'] = backing.UNKNOWN
            diaper['brand'] = 'Abena'
            # TODO: scrape this
            diaper['on_sale'] = possible.MAYBE
            diaper['retailer'] = 'Abena'
            diaper['scented'] = possible.NO
            diaper['tapes'] = 4
            diaper['title'] = title
            for variant in product.get('variants', []):
                size_label = variant.get('option1')
                if size_label == 'Junior':
                    continue
                id = variant.get('id')
                size = self.sizes.get(size_label)
                size_code = variant.get('option2')
                print(title, size_code)
                size_reference = reference.get(size_code)
                waist = size_reference.get('waist')
                diaper['capacity'] = self.reference.get(title).get(variant.get('option2')).get('capacity')
                diaper['id'] = id
                diaper['in_stock'] = possible.YES if variant.get("available") else possible.NO
                diaper['notes'] = []
                diaper['price'] = float(variant.get('price'))
                diaper['size'] = size
                diaper['units'] = size_reference.get(variant.get('option3'))
                diaper['url'] = f'https://abenausa.com/products/{handle}?variant={id}'
                diaper['waist_low'] = waist[0]
                diaper['waist_high'] = waist[1]
                yield diaper

