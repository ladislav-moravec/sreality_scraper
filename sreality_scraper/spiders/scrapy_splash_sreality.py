import scrapy
import json

class FlatSpider(scrapy.Spider):
    name = 'sreality_splash'

    start_urls = ['https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=' + str(100) + '&page='+str(x)+''for x in range(1, 6)]

    def parse(self, response):
         jsonresponse = response.json()
         for item in jsonresponse["_embedded"]['estates']:
             yield scrapy.Request( 'https://www.sreality.cz/api' + item['_links']['self']['href'] ,
                          callback=self.parse_flat)

    def parse_flat(self, response):
        jsonresponse = response.json()
        flat = FlatItem()
        flat['title'] = jsonresponse['name']['value']
        #item["ADDRESS"] = jsonresponse['locality']['value']

        for images in jsonresponse['_embedded']['images']:
            if images['_links']['dynamicDown']:
                tmp = images['_links']['dynamicDown']['href'].replace('{width}', '400')
                tmp = tmp.replace('{height}', '300')
                flat['image_urls'] = tmp
                break

        yield flat

