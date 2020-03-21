# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from web_scraper.items import WebScraperItem
from datetime import datetime

# from datetime import datatime

startpage_links = [
    "https://www.dr.dk/nyheder/allenyheder/indland",
    "https://www.dr.dk/nyheder/allenyheder/udland",
    "https://www.dr.dk/nyheder/allenyheder/penge",
    "https://www.dr.dk/nyheder/allenyheder/politik",
    "https://www.dr.dk/nyheder/allenyheder/sport",
    "https://www.dr.dk/nyheder/allenyheder/kultur",
    "https://www.dr.dk/nyheder/allenyheder/viden",
    "https://www.dr.dk/nyheder/allenyheder/mitliv",
    "https://www.dr.dk/nyheder/allenyheder/p4/bornholm",
    "https://www.dr.dk/nyheder/allenyheder/p4/fyn",
    "https://www.dr.dk/nyheder/allenyheder/p4/kbh",
    "https://www.dr.dk/nyheder/allenyheder/p4/vest",
    "https://www.dr.dk/nyheder/allenyheder/p4/nord",
    "https://www.dr.dk/nyheder/allenyheder/p4/sjaelland",
    "https://www.dr.dk/nyheder/allenyheder/p4/syd",
    "https://www.dr.dk/nyheder/allenyheder/p4/trekanten",
    "https://www.dr.dk/nyheder/allenyheder/vejret",
]


class Drspider(scrapy.Spider):
    name = "dr_spider"

    # TODO get all the startpage links
    # These can be found back in time by adding /DDMMYYYY to the url of the data in question

    custom_settings = {
        "LOG_FILE": f"data/logs/{name}.log",
        "VISITED_FILTER_PATH": f"data/{name}.filter",
        "NEVER_CACHE": startpage_links,
        "LOG_LEVEL": "INFO",
        "BOT_NAME": name,
    }

    def __init__(self, category=None, *args, **kwargs):
        super(Drspider, self).__init__(*args, **kwargs)

        self.section_css = ".dre-section-label__title::text"
        self.author_css = ".dre-article-byline__author span::text"
        self.date_css = ".dre-article-byline__date::attr(datetime)"
        self.title_css = ".dre-article-title__title::text"
        self.title_summary_css = ".dre-article-title__summary::text"
        self.image_caption_css = ".dre-image-caption::text"
        self.article_body_css = (
            ".dre-article-body__paragraph::text"  # needs an getall()
        )

    def choose_follow_css(self, response):
        startpage_follow_css = ".heading-small a::attr(href)"
        article_follow_css = ".dre-teaser a::attr(href)"

        if response.url in startpage_links:
            return startpage_follow_css

        return article_follow_css

    def start_requests(self):
        urls = startpage_links
        for url in urls:
            print(url)
            yield scrapy.Request(
                # The "dont_cache" ise used by job persistence middleware
                url=url,
                callback=self.parse,
                meta={"dont_cache": True},
            )

    def parse(self, response):
        # TODO get the css to follow from the frontpage
        follow_css = self.choose_follow_css(response)
        for next_page in response.css(follow_css).getall():
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_article)

    def parse_article(self, response):

        loader = self.default_itemload(response)

        yield loader.load_item()

        follow_css = self.choose_follow_css(response)
        # yield response.css(follow_css).getall()
        if follow_css:
            for next_page in response.css(follow_css).getall():
                # generate Requests of all the links to follow
                if next_page is not None:
                    yield response.follow(next_page, callback=self.parse_article)

    def default_itemload(self, response):
        loader = ItemLoader(item=WebScraperItem(), response=response)

        # TODO create the item.py with the default itemloader with input
        loader.add_value("scrape_date", datetime.now())
        loader.add_value("url", response.url)
        # Item css selectors, supplied by subclasses
        loader.add_css("section", self.section_css)
        loader.add_css("author", self.author_css)
        loader.add_css("date", self.date_css)
        loader.add_css("title", self.title_css)
        loader.add_css("title_summary", self.title_summary_css)
        loader.add_css("image_caption", self.image_caption_css)
        loader.add_css("article_body", self.article_body_css)

        return loader
