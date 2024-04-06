import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class BytySpider(CrawlSpider):
    name = "idnes"
    allowed_domains = ["reality.idnes.cz"]
    start_urls = ["https://reality.idnes.cz/s/byty/"]

    rules = (
        Rule(LinkExtractor(allow=(r"page=",))),
        Rule(LinkExtractor(allow=(r"detail",)), callback="parse_item")
    )

    def parse_item(self, response):
        pass
