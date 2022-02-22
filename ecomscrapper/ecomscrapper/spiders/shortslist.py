import json
import scrapy


class ShortslistSpider(scrapy.Spider):
    name = 'shortslist'
    allowed_domains = ['in.seamsfriendly.com']
    start_urls = {'https://services.mybcapps.com/bc-sf-filter/filter?t=1645525851722&_=pf&shop=seamsfriendly-india'
                  '.myshopify.com&page=3&limit=24&sort=manual&display=grid&collection_scope=273158144189&tag'
                  '=&product_available=true&variant_available=true&build_filter_tree=false&check_cache=false&callback'
                  '=BoostPFSFilterCallback&event_type=page'}

    def parse(self, response, **kwargs):
        with open(response.body, 'r') as j:
            data = json.loads(j.read())
        yield from data['inventory_quantity']['image']['price']['manual']

        next_page = data['inventory_quantity']['nextPageURL']
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)