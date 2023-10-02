# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import json


class PricePipeline:
    minPrice = 0.0
    maxPrice = 10.0

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price = -1
        if adapter.get("salePrice"):
            price = adapter["salePrice"]
        elif adapter.get("originalPrice"):
            price = adapter["originalPrice"]
        else:
            raise DropItem

        if self.minPrice < price < self.maxPrice:
            return item
        else:
            raise DropItem


class FreeShippingPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("free_shipping"):
            if adapter["free_shipping"]:
                return item
            else:
                raise DropItem
        else:
            raise DropItem


class RatingPipeline:
    minRating = 4

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('rating'):
            if adapter['rating'] >= self.minRating:
                return item
            else:
                raise DropItem
        else:
            raise DropItem


class JsonWriterPipeline:
    file = None

    def open_spider(self, spider):
        try:
            self.file = open("items.jsonl", "w")
        except OSError:
            self.file = None

    def close_spider(self, spider):
        if self.file is not None:
            self.file.close()

    def process_item(self, item, spider):
        if self.file is None:
            return item

        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
