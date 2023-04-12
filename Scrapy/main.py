import json

import scrapy
from scrapy.item import Item, Field, Spider
from scrapy.crawler import CrawlerProcess
from itemadapter import ItemAdapter
import json

class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()


class AuthorItem(Item):
    fullname = Field()
    date_born = Field()
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
            json.dump(self.quotes, fh)
        with open("authors.json", "w", encoding='utf-8') as fh:
            json.dump(self.authors, fh)

class MainSpider(scrapy.Spider):
    name = "main_spider"
    allowed_domains = ["http://quotes.toscrape.com/"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {"FEED_":}

    def parser(self, response, *arrgs):
        for el in response.xpath("/html//div@clas="):
            tags = [e.strip() for e in el.xpath("div@clas='tags']/a[@class")]
            author = el.xpath("span/small[class='author'")
            quote = el.xpath("span@class='text']/text()")
            yield QuoteItem(tags = tags, author = author, quote = quote)
            yield response.follow(url= self.start_urls[0], callback = self.pars_author)

    def parse_author(self, response, *args):
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath("")
        date_born = content.xpath("")
        born_location = content.xpath("")
        description = content.xpath("")
        yield AuthorItem(fullname = fullname, )



if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MainSpider)
    process.start()