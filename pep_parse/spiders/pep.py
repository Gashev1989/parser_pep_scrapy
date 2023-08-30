import scrapy

from pep_parse.items import PepParseItem
from pep_parse.settings import PATTERN, PEP_DOMAIN, PEP_START_URL, SPIDER_NAME


class PepSpider(scrapy.Spider):
    name = SPIDER_NAME
    allowed_domains = [PEP_DOMAIN]
    start_urls = [PEP_START_URL]

    def parse(self, response):
        all_peps = response.css('tbody tr a[href^="pep-"]')
        for pep_link in all_peps:
            pep_link = pep_link.css('a::attr(href)').get() + '/'
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        text_match = PATTERN.search((title))
        data = {
            'number': text_match.group('number'),
            'name': text_match.group('name'),
            'status': response.css('dt:contains("Status")+dd abbr::text').get()
        }
        yield PepParseItem(data)
