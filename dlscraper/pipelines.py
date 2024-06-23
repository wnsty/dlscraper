# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem # type: ignore


class DlscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price = adapter.get('price')
        units = adapter.get('units')
        capacity = adapter.get('capacity')

        if price is None:
            raise DropItem(f"Missing price in {item}")
        
        if units is None:
            raise DropItem(f"Missing units in {item}")

        if capacity is None:
            raise DropItem("Missing capacity in {item}")

        unit_price = price / units
        ml_per_unit_price = capacity / unit_price

        adapter['unit_price'] = unit_price
        adapter['ml_per_unit_price'] = ml_per_unit_price
        adapter['score'] = ml_per_unit_price / unit_price

        return item


class ABUPipeline:
    def process_item(self, item, spider):
        return item