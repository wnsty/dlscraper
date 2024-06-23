import time
import scrapy # type: ignore

import xml.etree.ElementTree as ET
from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes

class NorthshoreSpider(scrapy.Spider):
    '''
    This spider is incomplete.
    '''
    name = "northshore"
    allowed_domains = ["www.northshorecare.com"]
    start_urls = ["https://www.northshorecare.com/sitemap.xml"]
    product_urls = [
        "northshore-megamax-tab-style-briefs",
        "northshore-megamax-airlock-tab-style-briefs",
        "northshore-megamax-airlock-lite-tab-style-briefs",
        "northshore-airsupreme-tab-style-briefs",
        "northshore-supreme-tab-style-briefs",
        "northshore-megamax-air-tab-style-briefs",
    ]
    sizes = {
        "X-Small, 18 - 30 in.": sizes.XSMALL,
        "Small, 24 - 34 in.": sizes.SMALL,
        "Medium, 32 - 44 in.": sizes.MEDIUM,
        "Large, 42 - 54 in.": sizes.LARGE,
        "X-Large, 50 - 60 in.": sizes.XLARGE,
        "2X-Large, 60 - 76 in.": sizes.XLARGEPLUS,
    }
    units = {
        "Case/48 (4/12s) - Best Value!": 48,
        "Pack/12": 12,
        "Trial Pack/4": 4,
        "Case/40 (4/10s) - Best Value!": 40,
        "Pack/10": 10,
        "Case/32 (4/8s) - Best Value!": 32,
        "Pack/8": 8,
    }
    waists = {
        "X-Small, 18 - 30 in.": {
            "low": 18,
            "high": 30,
        },
        "Small, 24 - 34 in.": {
            "low": 24,
            "high": 34,
        },
        "Medium, 32 - 44 in.": {
            "low": 32,
            "high": 44,
        },
        "Large, 42 - 54 in.": {
            "low": 42,
            "high": 54,
        },
        "X-Large, 50 - 60 in.": {
            "low": 50,
            "high": 60,
        },
        "2X-Large, 60 - 76 in.": {
            "low": 60,
            "high": 76,
        },
    }

    def parse(self, response):
        urlset = ET.fromstring(response.text)

        for url in urlset:
            loc = url[0].text
            for product_url in self.product_urls:
                if loc.endswith(product_url):
                    continue
                if 'product-no-longer-available' in loc:
                    continue
                if product_url in loc:
                    yield {
                        "url": loc,
                        "price": 1,
                        "units": 1,
                        "capacity": 1,
                    }
                    
    def parse_diaper(self, response):
        diaper = Diaper()
        diaper['backing'] = backing.PLASTIC
        diaper['brand'] = 'Northshore'
        diaper['capacity'] = 6500
        diaper['id'] = -1
        diaper['in_stock'] = possible.NO
        diaper['notes'] = []
        # TODO: scrape this
        diaper['on_sale'] = possible.MAYBE
        diaper['price'] = 1
        diaper['retailer'] = 'NorthShore'
        diaper['scented'] = possible.NO
        diaper['size'] = sizes.MEDIUM
        diaper['tapes'] = 4
        diaper['title'] = 'MegaMax'
        diaper['units'] = 1
        diaper['url'] = response.url
        diaper['waist_low'] = 0
        diaper['waist_high'] = 100
        yield diaper