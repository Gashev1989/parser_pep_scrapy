import csv
import datetime as dt
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


class PepParsePipeline:
    def open_spider(self, spider):
        self.result = {}

    def process_item(self, item, spider):
        status = item["status"]
        self.result[status] = self.result.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        now = dt.datetime.now().strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now}.csv'
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        file_path = results_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', dialect='unix')
            writer.writerows(
                [
                    ("Статус", "Количество"),
                    *self.result.items(),
                    ("Total", sum(self.result.values()))
                ]
            )
