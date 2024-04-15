from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..postgresql.put_to_db import put_to_db


class BytySpider(CrawlSpider):
    counter = 0
    name = "idnes"
    allowed_domains = ["reality.idnes.cz"]
    start_urls = ["https://reality.idnes.cz/s/byty/"]

    rules = (
        Rule(LinkExtractor(allow=(r"page=",))),
        Rule(LinkExtractor(allow=(r"detail",)), callback="parse_item")
    )

    def parse_item(self, response):
        title = response.css(".b-detail__title > span::text").get()
        price = response.css(".b-detail__price > strong::text").get()
        image_urls = response.css('div.b-gallery__img-lg.carousel__wrap img[data-lazy]::attr(data-lazy)').getall()
        print(title)
        print(price)
        print(image_urls)

        put_to_db("idnes_reality", title, price, image_urls)
        self.counter += 1

        if self.counter >= 500:
            self.crawler.engine.close_spider(self, "Reached 500 items.")

    def closed(self, reason):
        print("Spider closed:", reason)
