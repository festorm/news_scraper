# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# https://docs.scrapy.org/en/latest/topics/loaders.html

import scrapy
import w3lib.html  # use for removing tags
from scrapy.loader.processors import Join, MapCompose
from datetime import datetime


def check_not_none(x):
    """
    remove all empty strings
    """
    return x if x else None


def get_datetime(dateobj):
    """
    Reformat the date from the byline
    """
    date = datetime.strptime(dateobj, "%Y-%m-%dT%H:%M:%S+00:00")

    return datetime.strftime(date, "%Y-%m-%d %H:%M")


class WebScraperItem(scrapy.Item):
    scrape_date = scrapy.Field()
    url = scrapy.Field()

    section = scrapy.Field(
        input_processor=MapCompose(w3lib.html.remove_tags, str.strip, check_not_none),
        output_processor=Join(),
    )

    author = scrapy.Field(
        input_processor=MapCompose(w3lib.html.remove_tags, str.strip, check_not_none),
        output_processor=Join(),
    )

    date = scrapy.Field(
        input_processor=MapCompose(
            w3lib.html.remove_tags, str.strip, check_not_none, get_datetime
        )
    )

    title = scrapy.Field(
        input_processor=MapCompose(w3lib.html.remove_tags, str.strip, check_not_none)
    )

    title_summary = scrapy.Field(
        input_processor=MapCompose(w3lib.html.remove_tags, str.strip, check_not_none)
    )

    image_caption = scrapy.Field(
        input_processor=MapCompose(w3lib.html.remove_tags, str.strip, check_not_none),
        output_processor=Join(),
    )

    text = scrapy.Field(
        input_processor=MapCompose(w3lib.html.remove_tags, str.strip, check_not_none),
        output_processor=Join(),
    )
