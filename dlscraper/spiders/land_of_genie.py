import re
import scrapy # type: ignore

from dlscraper.enum import backing, possible, sizes
from dlscraper.spiders import shopify


class LandOfGenieSpider(shopify.ShopifySpider):
    name = "land_of_genie"
    allowed_domains = ["landofgenie.com"]
    start_urls = ["https://landofgenie.com/products.json?limit=1000"]
    base_product_url = 'https://landofgenie.com/products/'
    units_pattern = re.compile(r'(\d) (Sample|Pack)')

    def backing(self, product):
        return backing.PLASTIC

    def brand(self, product):
        return "Landofgenie"
    
    def capacity(self, response, variant, diaper_variant):
        return 5000
    
    # TODO: scrape this
    def in_stock(self, variant):
        return possible.MAYBE

    def is_valid(self, product):
        return product['product_type'] == '尿布'
    
    # TODO: scrape this
    def on_sale(self, response):
        possible.MAYBE
    
    def retailer(self, product):
        return "Landofgenie"
    
    def scented(self, variant):
        return possible.NO
    
    def size(self, variant):
        return variant['option1']
    
    def tapes(self, product):
        return 4
    
    def title(self, product):
        return product['title']
    
    def units(self, variant):
        option2 = variant['option2']
        search = self.units_pattern.search(option2)
        if search.group(2) == 'Sample':
            return int(search.group(1))
        else:
            return int(search.group(1)) * 10
    
    def waist(self, diaper_variant, variant):
        if diaper_variant['size'] == sizes.MEDIUM:
            return {
                "low": 28,
                "high": 38,
            }
        else:
            return {
                "low": 36,
                "high": 46,
            }