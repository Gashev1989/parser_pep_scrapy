import re

import scrapy

from pep_parse.items import PepParseItem


PATTERN = re.compile(r"^PEP\s(?P<number>\d+)[\s–]+(?P<name>.*)")


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('tbody tr a[href^="pep-"]')
        for pep_link in all_peps:
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
