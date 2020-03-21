# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class WebScraperPipeline(object):
    def process_item(self, item, spider):
        url = item["url"][0]
        if hasattr(spider, "scraped_urls"):
            if url in spider.scraped_urls:
                spider.logger.info("Duplicated")
                raise DropItem()
            else:
                spider.scraped_urls.add(url)
        return item
