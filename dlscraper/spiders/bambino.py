import re

from dlscraper.enum import backing, possible, sizes
from dlscraper.spiders import shopify


class BambinoSpider(shopify.ShopifySpider):
    name = "bambino"
    allowed_domains = ["bambinodiapers.com"]
    start_urls = ["https://bambinodiapers.com/products.json?limit=1000"]
    base_product_url = "https://bambinodiapers.com/products/"
    # TODO: scrape capacities
    capacities = {
        "Bellissimo All Over Print Diapers": 5000,
        "Bellissimo Landing Zone Print Diapers": 5000,
        "Bianco All White Diapers": 4500,
        "Bianco Ultra Stretch All White Diapers": 4500,
        "Bloomeez All Over Print Diapers": 5000,
        "Catstronaut All Over Print Diapers": 5000,
        "Classico All Over Print Diapers": 4500,
        "Classico Landing Zone Print Diapers": 4500,
        "Cloudee All Over Print Diapers": 4500,
        "Magnifico All Over Print Diapers": 4500,
        "TotalDry X-Plus Briefs": 3500,
    }
    bambino_sizes = {
        "M": sizes.MEDIUM,
        "L": sizes.LARGE,
        "XL": sizes.XLARGE,
    }
    size_pattern = re.compile(r'(M|L|XL) ')
    waist_low_pattern = re.compile(r'\((\d{2})\"')
    waist_high_pattern = re.compile(r'(\d{2})\"\)')
    units_pattern = re.compile(r'of (\d{1,2})')


    def backing(self, product):
        return backing.PLASTIC

    def brand(self, product):
        if product.get('title') == 'TotalDry X-Plus Briefs':
            return 'TotalDry'
        return "Bambino"

    def capacity(self, response, variant, diaper_variant):
        title = diaper_variant.get("title")
        return self.capacities.get(title)

    def is_valid(self, product):
        product_type = product.get("product_type")
        return (
            product_type == "All Over Print Diaper"
            or product_type == "Landing Zone Print Diaper"
            or product_type == "All White Diaper"
            or product_type == "buildabx"
            or product_type == "TotalDry Briefs"
        )

    def on_sale(self, response):
        return possible.MAYBE

    def retailer(self, product):
        return "Bambino"

    def scented(self, variant):
        return possible.NO

    def size(self, variant):
        size_match = self.size_pattern.search(variant.get('title')).group(1)
        if size_match is None:
            return sizes.UNKOWN
        return self.bambino_sizes.get(size_match)

    def tapes(self, product):
        return 4
    
    def title(self, product):
        return product.get('title')
    
    def units(self, variant):
        return int(self.units_pattern.search(variant.get('title')).group(1))
        
    def waist(self, diaper_variant, variant):
        title = variant.get('title')
        return {
            "low": int(self.waist_low_pattern.search(title).group(1)),
            "high": int(self.waist_high_pattern.search(title).group(1)),
        }