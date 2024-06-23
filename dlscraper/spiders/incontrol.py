import re
import scrapy  # type: ignore
import time


from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.by import By
from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes


class IncontrolSpider(scrapy.Spider):
    name = "incontrol"
    allowed_domains = ["incontroldiapers.com"]
    start_urls = ["https://incontroldiapers.com/adult-disposable-diaper/"]
    ignored_urls = {
        "https://incontroldiapers.com/felicity-super-absorbent-underwear/",
        "https://incontroldiapers.com/tranquility-swimmates-disposable-swim-briefs/",
        "https://incontroldiapers.com/molicare-premium-mobile-underwear/",
    }
    driver = None
    units_pattern = re.compile(r'\d{1,2}')
    units = {
        "Abena Abri-Form Premium Incontinence Briefs": {
            "Small": {
                "Bag": 22,
                "Case": 66
            },
            "Medium": {
                "Bag": 21,
                "Case": 84,
            },
            "Large": {
                "Bag": 18,
                "Case": 72,
            },
            "XLarge": {
                "Bag": 12,
                "Case": 48,
            },
            "XLarge+": {
                "Bag": 10,
                "Case": 40,
            },
        },
        "Tena Slip Active ULTIMA Incontinence Briefs": {
            "Medium": {
                "Bag": 21,
                "Case": 63,
            },
            "Large": {
                "Bag": 21,
                "Case": 63,
            },
        },
        "Tena Slip Maxi (European) Incontinence Briefs": {
            "Small": {
                "Bag": 24,
                "Case": 72,
            },
            "Medium": {
                "Bag": 24,
                "Case": 72,
            },
            "Large": {
                "Bag": 22,
                "Case": 66,
            },
        }
    }
    capacities = {
        "InControl BeDry EliteCare Premium Incontinence Briefs": 10000,
        "InControl BeDry Night Premium Incontinence Briefs": 12000,
        "Incontrol Elite Youth Incontinence Diapers": 2700,
        "InControl BeDry Premium Incontinence Briefs": 7500,
        "Incontrol Essential Incontinence Briefs": 4300,
        "InControl Active Air Incontinence Briefs": 4250,
        "Incontrol Premium Nights Briefs with Whiff-X": 5600,
        "Abena Abri-Form Premium Incontinence Briefs": 3600,
        "Tena Slip Active ULTIMA Incontinence Briefs": 3600,
        "Tena Slip Maxi (European) Incontinence Briefs": 3000,
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(IncontrolSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider

    def spider_opened(self):
        self.driver = webdriver.Firefox()

    def brand(self, title):
        if "InControl" in title or "Incontrol" in title:
            return "InControl"
        elif "Molicare" in title:
            return "Molicare"
        elif "Tranquility" in title:
            return "Tranquility"
        elif "Abena" in title:
            return "Abena"
        elif "Tena" in title:
            return "Tena"

    def get_size(self, label):
        if "XS" in label or "X-Small" in label:
            return sizes.XSMALL
        if "2X-Large" in label or "XXL" in label:
            return sizes.XLARGEPLUS
        if "X-Large" in label or "XL" in label:
            return sizes.XLARGE
        if "Large" in label:
            return sizes.LARGE
        if "Medium" in label:
            return sizes.MEDIUM
        if "Small" in label:
            return sizes.SMALL

    def parse(self, response):
        for url in response.css(".card-title a::attr(href)").getall():
            if url in self.ignored_urls:
                continue
            self.driver.get(url)
            id = self.driver.find_element(
                By.CSS_SELECTOR,
                ".productView-options > form:nth-child(1) > input:nth-child(2)",
            ).get_attribute("value")
            title = self.driver.find_element(By.CSS_SELECTOR, ".productView-title").text
            size_labels = self.driver.find_elements(By.CSS_SELECTOR, '.productView-options > form:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div > label')
            units_labels = self.driver.find_elements(By.CSS_SELECTOR, '.productView-options > form:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div > label')
            for size_label in size_labels:
                size = self.get_size(size_label.text)
                size_label.click()
                for units_label in units_labels:
                    units_match = self.units_pattern.search(units_label.text)
                    units = int(
                        self.units.get(title).get(units_label.text)
                        if units_match is None
                        else int(units_match.group(0))
                    )
                    units_label.click()
                    time.sleep(2)
                    price_label = self.driver.find_element(
                        By.CSS_SELECTOR,
                        ".productView-price > div:nth-child(3) > span:nth-child(3)",
                    )
                    diaper = Diaper()
                    # TODO: scrape this?
                    diaper["backing"] = backing.UNKNOWN
                    diaper["brand"] = self.brand(title)
                    diaper["capacity"] = self.capacities.get(title)
                    diaper["id"] = id
                    # TODO: scrape this
                    diaper["in_stock"] = possible.MAYBE
                    diaper["notes"] = [
                        "may show incorrect tapes",
                        "may show incorrect price :)",
                    ]
                    # TODO: scrape this
                    diaper["on_sale"] = possible.MAYBE
                    diaper["price"] = float(price_label.text[4:])
                    diaper["retailer"] = "Rearz"
                    # TODO: catalog this
                    diaper["scented"] = possible.MAYBE
                    diaper["size"] = size
                    diaper["tapes"] = 4
                    diaper["title"] = title
                    diaper["units"] = units
                    diaper["url"] = url
                    diaper["waist_low"] = 0
                    diaper["waist_high"] = 100
                    yield diaper

    def closed(self, reason):
        self.driver.close()
