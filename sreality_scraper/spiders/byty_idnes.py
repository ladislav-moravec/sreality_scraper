from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


# import sys
# print(sys.path)
# sys.path.append(r"C:\Users\morav\PycharmProjects\sreality_scraper")
# print(sys.path)

from ..postgresql.put_to_db import put_to_db


class BytySpider(CrawlSpider):
    name = "idnes"
    allowed_domains = ["reality.idnes.cz"]
    start_urls = ["https://reality.idnes.cz/s/byty/"]

    rules = (
        Rule(LinkExtractor(allow=(r"page=",))),
        Rule(LinkExtractor(allow=(r"detail",)), callback="parse_item")
    )


    def parse_item(self, response):
        """
        response.css(".b-detail__title > span::text").get()
        response.css(".b-detail__price > strong::text").get()
        response.css('div.b-gallery__img-lg.carousel__wrap img[data-lazy]::attr(data-lazy)').getall()
        """
        title = response.css(".b-detail__title > span::text").get()
        price = response.css(".b-detail__price > strong::text").get()
        image_urls = response.css('div.b-gallery__img-lg.carousel__wrap img[data-lazy]::attr(data-lazy)').getall()
        print(title)
        print(price)
        print(image_urls)

        # yield {
        #     "title": response.css(".b-detail__title > span::text").get(),
        #     "price": response.css(".b-detail__price > strong::text").get(),
        #     "image_urls": response.css('div.b-gallery__img-lg.carousel__wrap img[data-lazy]::attr(data-lazy)').getall(),
        # }

        put_to_db("idnes_reality",title, price, image_urls)
