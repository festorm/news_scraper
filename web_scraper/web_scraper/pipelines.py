# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class WebScraperPipeline(object):

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        url = item["url"][0]

        if url in self.urls_seen:
            spider.logger.info(f"Duplicated: {url}")
            raise DropItem()
        else:
            self.urls_seen.add(url)
            return item

class CheckForTextPipeline(object):

    def process_item(self, item, spider):
        if item.get("text"):
            return item
        else:
            raise DropItem("Missing text")