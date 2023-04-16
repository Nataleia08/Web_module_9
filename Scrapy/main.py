import json

import scrapy
from scrapy.item import Item, Field
# import Spider
from scrapy.crawler import CrawlerProcess
from itemadapter import ItemAdapter
import json
import requests


class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class MainPipline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "fullname" in adapter.keys():
            self.authors.append(adapter.asdict())
        if "quote" in adapter.keys():
            self.quotes.append(adapter.asdict())
        return item

    def close_spider(self, spider):
        with open("quotes.json", "w", encoding='utf-8') as fh:
            json.dump(self.quotes, fh, ensure_ascii=False)
        with open("authors.json", "w", encoding='utf-8') as fh:
            json.dump(self.authors, fh, ensure_ascii=False)


class MainSpider(scrapy.Spider):
    name = "main_spider"
    allowed_domains = ["quotes.toscrape.com/"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {"ITEM_PIPELINES": {MainPipline: 100}}

    def parse(self, response, *args):
        for el in response.xpath("/html//div[@class='quote']"):
            tags = [e.strip() for e in el.xpath("div[@class='tags']/a[@class='tag']/text()").extract()]
            author = el.xpath("span/small[@class='author']/text()").get().strip()
            quote = el.xpath("span[@class='text']/text()").get().strip()
            yield response.follow(url=self.start_urls[0] + el.xpath("span/a/@href").get().strip(), callback=self.parse_author)
            yield QuoteItem(tags=tags, author=author, quote=quote)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link is not None:
            yield response.follow(url=self.start_urls[0] + next_link.strip(), callback = self.parse)
                #scrapy.Request(url=self.start_urls[0] + next_link.strip())

    def parse_author(self, response, *args):
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath("h3[@class='autor-title']/text()").get().strip()
        born_date = content.xpath("p/span[@class='author-born-date']/text()").get().strip()
        born_location = content.xpath("p/span[@class='author-born-location']/text()").get().strip()
        description = content.xpath("div[@class='author-description']/text()").get().strip()
        return AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MainSpider)
    process.start()
    process.join()
    print("The end")
