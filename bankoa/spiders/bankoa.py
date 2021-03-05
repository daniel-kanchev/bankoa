import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bankoa.items import Article


class BankoaSpider(scrapy.Spider):
    name = 'bankoa'
    start_urls = ['https://www.bankoa.es/']

    def parse(self, response):
        links = response.xpath('//div[@id="noticias"]//h3/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@id="over-hero"]//h2/text()').get()
        if title:
            title = title.strip()
        else:
            return

        date = response.xpath('//div[@class="fecha"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@id="over-hero"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[3:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
