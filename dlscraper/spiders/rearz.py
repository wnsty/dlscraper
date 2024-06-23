import re
import scrapy  # type: ignore
import time

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.by import By
from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes

class RearzSpider(scrapy.Spider):
    name = "rearz"
    allowed_domains = ["rearz.ca"]
    start_urls = ["https://rearz.ca/diapers/disposables/?limit=100"]
    ingored_urls = [
        "https://rearz.ca/rearz-diaper-lover-stack/",
        "https://rearz.ca/rearz-dl-weekend-warrior-pack/",
        "https://rearz.ca/rearz-ultimate-printed-mixed-pack/",
        "https://rearz.ca/large-diaper-pail-deodorizer-discs-40/",
        "https://rearz.ca/baby-girl-mixed-case/",
        "https://rearz.ca/incontrol-booster-pads-unscented/",
        "https://rearz.ca/lil-mixed-diaper-case/",
        "https://rearz.ca/felicity-super-absorbent-incontinence-underwear/",
        "https://rearz.ca/rearz-overnight-adult-booster-pads/",
    ]
    driver = None
    units_pattern = re.compile(r'\d{1,2}')
    reference = {
        "Select - Vintage Adult Diapers": {
            "sizes": {
                "Medium": {
                    "low": 26,
                    "high": 47,
                    "units": {
                        "bag": 12,
                        "case": 36,
                    },
                },
                "Large": {
                    "low": 30,
                    "high": 54,
                    "units": {
                        "bag": 12,
                        "case": 36,
                    },
                },
            },
            "Bag": 12,
            "Case": 36,
            "tapes": 2,
            "backing": backing.PLASTIC,
            "scented": possible.NO,
            "capacity": 3800,
        },
        "InControl BeDry Night Premium Incontinence Briefs": {
            "capacity": 12000,
        },
        "Daydreamer Adult Diapers - 2XL": {
            "capacity": 11000,
        },
        "Daydreamer Adult Diapers": {
            "capacity": 11000,
        },
        "Mega Critter Caboose Adult Diapers": {
            "capacity": 11000,
        },
        "Mega Safari Adult Diapers": {
            "capacity": 11000,
        },
        "Princess Pink Adult Diapers": {
            "capacity": 8500,
        },
        "Mega Inspire+ Adult Diapers": {
            "capacity": 11000,
        },
        "Rearz Lil' Monsters Adult Diapers": {
            "capacity": 6000,
        },
        "Mega Barnyard Adult Diapers": {
            "capacity": 11000,
        },
        "Lil Squirts Adult Diapers - Splash": {
            "Bag": 16,
            "Case": 48,
            "capacity": 6000,
        },
        "Mega Dinosaur Adult Diapers": {
            "capacity": 11000,
        },
        "Incontrol Elite Hybrid Briefs - XS": {
            "capacity": 2700,
        },
        "Rearz Alpaca Adult Diapers": {
            "capacity": 8500,
        },
        "Rearz Lil Bella Adult Diapers": {
            "Bag": 16,
            "Case": 48,
            "capacity": 6000,
        },
        "Incontrol Essential Incontinence Briefs": {
            "capacity": 4300,
        },
        "Mega Mermaid Tales Adult Diapers": {
            "capacity": 11000,
        },
        "Incontrol Premium Nights Briefs": {
            "Trial": 2,
            "Bag": 12,
            "Case": 36,
            "capacity": 5600,
        },
        "Incontrol Active Air Incontinence Briefs": {
            "capacity": 4200,
        },
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(RearzSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened,  signal=signals.spider_opened)
        return spider

    def spider_opened(self):
        self.driver = webdriver.Firefox()

    def get_size(self, label):
        if "XS" in label or "X-Small" in label:
            return sizes.XSMALL
        if "2X-Large" in label:
            return sizes.XLARGEPLUS
        if "X-Large" in label:
            return sizes.XLARGE
        if "Large" in label:
            return sizes.LARGE
        if "Medium" in label:
            return sizes.MEDIUM
        if "Small" in label:
            return sizes.SMALL

    def parse(self, response):
        for url in response.css(".card-title a::attr(href)").getall():
            if url in self.ingored_urls:
                continue
            self.driver.get(url)
            id = self.driver.find_element(
                By.CSS_SELECTOR,
                ".productView-options > form:nth-child(1) > input:nth-child(2)",
            ).get_attribute("value")
            title = self.driver.find_element(By.CSS_SELECTOR, ".productView-title").text
            option1 = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".productView-options > form:nth-child(1) > div:nth-child(4) > div:nth-child(1) > label",
            )
            option2 = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".productView-options > form:nth-child(1) > div:nth-child(4) > div:nth-child(2) > label",
            )
            size_labels = option1[1:] if option1[0].text == "Size *" else option2[1:]
            units_labels = (
                option2[1:] if option2[0].text == "Quantity *" else option1[1:]
            )
            for size_label in size_labels:
                size = self.get_size(size_label.text)
                size_label.click()
                for units_label in units_labels:
                    units_match = self.units_pattern.search(units_label.text)
                    units = int(self.reference.get(title).get(units_label.text) if units_match is None else int(units_match.group(0)))
                    units_label.click()
                    time.sleep(2)
                    price_label = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "div.productView-price:nth-child(4) > div:nth-child(3) > span:nth-child(1)",
                    )
                    diaper = Diaper()
                    # TODO: scrape this?
                    diaper['backing'] = backing.UNKNOWN
                    diaper['brand'] = "Incontrol" if "InControl" in title else "Rearz"
                    diaper['capacity'] = self.reference.get(title).get('capacity')
                    diaper['id'] = id
                    # TODO: scrape this
                    diaper['in_stock'] = possible.MAYBE
                    diaper['notes'] = ["may show incorrect tapes", "may show incorrect price :)"]
                    # TODO: scrape this
                    diaper['on_sale'] = possible.MAYBE
                    diaper['price'] = float(price_label.text[3:])
                    diaper['retailer'] = "Rearz"
                    # TODO: catalog this
                    diaper['scented'] = possible.MAYBE
                    diaper['size'] = size
                    diaper['tapes'] = 4
                    diaper['title'] = title
                    diaper['units'] = units
                    diaper['url'] = url
                    diaper['waist_low'] = 0
                    diaper['waist_high'] = 100
                    yield diaper

    def closed(self, reason):
        self.driver.close()
