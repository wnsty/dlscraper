import scrapy # type: ignore

from dlscraper.items import Diaper
from dlscraper.enum import backing, possible, sizes

class AwwsocuteSpider(scrapy.Spider):
    name = "awwsocute"
    allowed_domains = ["www.awwsocute.com"]
    start_urls = [
        "https://www.awwsocute.com/diapers/53-6-pink-teddy-bear-diapers.html",
        "https://www.awwsocute.com/diapers/87-75-purple-teddy-bear-diapers.html",
    ]

    def parse(self, response):
        title = response.css('.h1::text').get()
        price_label = response.css('.current-price > span:nth-child(1)::attr(content)').get()
        diaper = Diaper()
        diaper['backing'] = backing.PLASTIC
        diaper['brand'] = 'AwwSoCute'
        diaper['capacity'] = 4000
        diaper['id'] = -1
        # TODO: scrape this
        diaper['in_stock'] = possible.MAYBE 
        diaper['notes'] = ['capacity may not be accurate']
        # TODO: scrape this
        diaper['on_sale'] = possible.MAYBE 
        diaper['price'] = float(price_label)
        diaper['retailer'] = 'AwwSoCute'
        diaper['scented'] = possible.NO
        diaper['size'] = sizes.MEDIUM
        diaper['tapes'] = 4
        diaper['title'] = title
        diaper['units'] = 10
        diaper['url'] = response.url
        diaper['waist_low'] = 30
        diaper['waist_high'] = 45
        yield diaper