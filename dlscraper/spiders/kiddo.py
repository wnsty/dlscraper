import json
import scrapy  # type: ignore

from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes


class KiddoSpider(scrapy.Spider):
    name = "kiddo"
    allowed_domains = ["us.kiddo-diapers.com"]
    start_urls = ["https://us.kiddo-diapers.com/products.json?limit=1000"]
    capacities = {
        'Kiddo Xtreme': 11500,
        'Kiddo Teddy Ultra': 6000,
        'Kiddo Lil Soaker': 5000,
        'Kiddo Little Sailor': 5000,
        "Kiddo Let's Build": 5000,
        'Kiddo Junior Plus Blue': 4500,
        'Kiddo Junior Plus Pink': 4500,
    }
    waists = {
        'Kiddo Xtreme': {
            "Medium": {
                "low": 28,
                "high": 39,
            },
            "Large": {
                "low": 39,
                "high": 51,
            },
            "XLarge": {
                "low": 45,
                "high": 57,
            }
        },
        'Kiddo Teddy Ultra': {
            "Medium": {
                "low": 28,
                "high": 39,
            },
            "Large": {
                "low": 39,
                "high": 51,
            },
        },
        'Kiddo Lil Soaker': {
            "Medium": {
                "low": 28,
                "high": 39,
            },
            "Large": {
                "low": 39,
                "high": 51,
            },
        },
        'Kiddo Little Sailor': {
            "Medium": {
                "low": 28,
                "high": 39,
            },
            "Large": {
                "low": 39,
                "high": 51,
            },
        },
        "Kiddo Let's Build": {
            "Medium": {
                "low": 28,
                "high": 39,
            },
            "Large": {
                "low": 39,
                "high": 51,
            },
            "XLarge": {
                "low": 45,
                "high": 57,
            }
        },
        'Kiddo Junior Plus Blue': {
            "Medium": {
                "low": 26,
                "high": 47,
            },
            "Large": {
                "low": 30,
                "high": 53,
            },
        },
        'Kiddo Junior Plus Pink': {
            "Medium": {
                "low": 26,
                "high": 47,
            },
            "Large": {
                "low": 30,
                "high": 53,
            },
        },
    }
    units = {
        "Pack": 10,
        "Case": 40,
    }
    tapes = {
        'Kiddo Xtreme': 4,
        'Kiddo Teddy Ultra': 2,
        'Kiddo Lil Soaker': 4,
        'Kiddo Little Sailor': 4,
        "Kiddo Let's Build": 4,
        'Kiddo Junior Plus Blue': 2,
        'Kiddo Junior Plus Pink': 2,
    }

    def parse(self, response):
        data = json.loads(response.text)
        for product in data.get("products", []):
            title = product.get("title")
            if product.get("product_type") != "Diapers" or title == "Pads Kiddo Mega booster":
                continue
            handle = product.get('handle')
            diaper = Diaper()
            if title == 'Kiddo Teddy Ultra':
                diaper['backing'] = backing.CLOTH
            else:
                diaper['backing'] = backing.PLASTIC
            diaper['brand'] = 'Kiddo'
            diaper['capacity'] = self.capacities.get(title)
            diaper['notes'] = []
            # TODO: scrape this
            diaper['on_sale'] = possible.MAYBE
            diaper['retailer'] = 'Kiddo'
            diaper['scented'] = possible.NO
            diaper['tapes'] = self.tapes.get(title)
            diaper['title'] = title
            for variant in product.get('variants', []):
                id = variant.get('id')
                size = variant.get('option1')
                waist = self.waists.get(title).get(size)
                diaper['id'] = id
                diaper['in_stock'] = possible.YES if variant.get("available") else possible.NO
                diaper['price'] = float(variant.get('price'))
                diaper['size'] = size
                diaper['units'] = self.units.get(variant.get('option2'))
                diaper['url'] = f'https://us.kiddo-diapers.com/products/{handle}?variant={id}'
                diaper['waist_low'] = waist.get('low')
                diaper['waist_high'] = waist.get('high')
                yield diaper
