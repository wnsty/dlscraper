from dlscraper.spiders.shopify import ShopifySpider
from dlscraper.enum import backing, possible


class AbuSpider(ShopifySpider):
    name = "abu"
    allowed_domains = ["us.abuniverse.com"]
    start_urls = ["https://us.abuniverse.com/products.json?limit=1000"]
    base_product_url = "https://us.abuniverse.com/products/"
    capacities = {
        "PeekABU": 7500,
        "LittlePawz": 5500,
        "Space™": 5500,
        "Little Kings": 7500,
        "Super Dry Kids": 4500,
        "DinoRawrZ": 6050,
        "AlphaGatorZ": 7500,
        "BunnyHopps 4-Tape": 6050,
        "Cushies™": 4500,
        "Simple Ultra": 7500,
        "Cloth-Backed Cushies™": 4500,
        "TinyTails": 7500,
        "Cushies Ultra": 6500,
    }
    # TODO: scrape waists
    waists = {
        "PeekABU": {
            "Medium": {"low": 31, "high": 36},
            "Large": {"low": 37, "high": 42},
            "XLarge": {"low": 43, "high": 46},
            "XLarge+": {"low": 43, "high": 64},
        },
        "LittlePawz": {
            "Small": {"low": 25, "high": 31},
            "Medium": {"low": 31, "high": 36},
            "Large": {"low": 37, "high": 44},
            "XLarge": {"low": 45, "high": 52},
        },
        "Space™": {
            "Small": {"low": 22, "high": 29},
            "Medium": {"low": 31, "high": 36},
            "Large": {"low": 37, "high": 44},
            "XLarge": {"low": 45, "high": 51},
        },
        "Little Kings": {
            "Medium": {"low": 31, "high": 36},
            "Large": {"low": 37, "high": 42},
            "XLarge": {"low": 43, "high": 48},
        },
        "Super Dry Kids": {
            "Small": {"low": 22, "high": 29},
            "Medium": {"low": 30, "high": 36},
            "Large": {"low": 37, "high": 42},
            "XLarge": {"low": 43, "high": 48},
        },
        "DinoRawrZ": {
            "Medium": {"low": 26, "high": 34},
            "Large": {"low": 35, "high": 41},
            "XLarge": {"low": 42, "high": 48},
        },
        "AlphaGatorZ": {
            "Medium": {"low": 31, "high": 36},
            "Large": {"low": 37, "high": 42},
            "XLarge": {"low": 43, "high": 48},
        },
        "BunnyHopps 4-Tape": {
            "Medium": {"low": 26, "high": 34},
            "Large": {"low": 35, "high": 41},
            "XLarge": {"low": 42, "high": 48},
        },
        "Cushies™": {
            "Small": {"low": 22, "high": 29},
            "Medium": {"low": 30, "high": 36},
            "Large": {"low": 37, "high": 42},
            "XLarge": {"low": 43, "high": 48},
        },
        "Simple Ultra": {
            "Medium": {"low": 31, "high": 36},
            "Large": {"low": 37, "high": 42},
            "XLarge": {"low": 43, "high": 48},
        },
        "Cloth-Backed Cushies™": {
            "Medium": {"low": 30, "high": 36},
            "Large": {"low": 37, "high": 42},
            "XLarge": {"low": 43, "high": 48},
        },
        "TinyTails": {
            "Small": {"low": 25, "high": 31},
            "Medium": {"low": 31, "high": 36},
            "Large": {"low": 37, "high": 44},
            "XLarge": {"low": 45, "high": 51},
        },
        "Cushies Ultra": {
            "Medium": {"low": 30, "high": 36},
            "Large": {"low": 37, "high": 42},
            "XLarge": {"low": 43, "high": 48},
        },
    }

    def finalize(self, variant):
        yield variant

        if variant.get("units") == 10:
            units = 40
            price = variant.get("price") * 4 * 0.8
            unit_price = price / units
            ml_per_unit_price = variant.get("capacity") / unit_price
            score = ml_per_unit_price / unit_price
            pack = variant.copy()
            pack["units"] = units
            pack["price"] = price
            pack["unit_price"] = unit_price
            pack["ml_per_unit_price"] = ml_per_unit_price
            pack["score"] = score
            yield pack

    def backing(self, product):
        return self.map_tags(
            product.get("tags"),
            backing.PLASTIC,
            backing.CLOTH,
            lambda t: t == "Plastic Backed",
        )

    def brand(self, product):
        return "ABUniverse"

    def capacity(self, response, variant, diaper_variant):
        capacity_str = response.css(
            "div.tw-flex:nth-child(8) > div:nth-child(2)::text"
        ).get()
        if capacity_str is None:
            return self.capacities(diaper_variant.get("title"))
        else:
            return int(capacity_str[:-2])

    def in_stock(self, variant):
        if variant.get("available"):
            return possible.YES
        else:
            return possible.NO

    def is_valid(self, product):
        product_type = product.get("product_type")

        if product_type != "Diapers":
            return False

        return not self.check_tags(product.get("tags"), lambda t: t == "Vaulted")

    def on_sale(self, response):
        if (
            response.css(".price.price--large.price--on-sale.price--show-badge").get()
            is None
        ):
            return possible.NO
        else:
            return possible.YES

    def retailer(self, product):
        return "ABUniverse"

    def scented(self, variant):
        if variant.get("option3") == "Scented":
            return possible.YES
        else:
            return possible.NO

    def size(self, variant):
        return variant.get("option2")

    def tapes(self, product):
        return self.map_tags(product.get("tags"), 4, 2, lambda t: t == "4 Tape")

    def title(self, product):
        return product.get("title")

    def units(self, variant):
        option1 = variant.get("option1")

        if option1 == "Pack - 10 Diapers":
            return 10
        else:
            return 2

    def waist(self, daiper_variant, variant):
        title = daiper_variant.get("title")
        size = daiper_variant.get("size")

        self.logger.info(title)

        return self.waists.get(title).get(size)
