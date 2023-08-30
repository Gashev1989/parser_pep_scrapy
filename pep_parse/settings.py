import re


BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

ROBOTSTXT_OBEY = True

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
PATTERN = re.compile(r"^PEP\s(?P<number>\d+)[\s–]+(?P<name>.*)")
PEP_DOMAIN = 'peps.python.org'
PEP_START_URL = 'https://peps.python.org/'
SPIDER_NAME = 'pep'

FEEDS = {
    "results/pep_%(time)s.csv": {
        "format": "csv",
        "fields": ["number", "name", "status"],
        "overwrite": True
    }
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}
