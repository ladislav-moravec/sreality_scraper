import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class BytySpider(CrawlSpider):
    name = "sreality"
    allowed_domains = ["sreality.cz"]
    start_urls = ["https://www.sreality.cz/hledani/prodej/byty"]

    rules = (
        Rule(LinkExtractor(allow=(r"strana=",))),
        Rule(LinkExtractor(allow=(r"detail",)), callback="parse_item")
    )

    def parse_item(self, response):
        pass
