# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from ..items import ProjectItem


HOST = "https://www.freelancer.com"


class Main(CrawlSpider):
    name = "freelancer"
    allowed_domains = ["freelancer.com"]
    start_urls = [HOST + "/job/"]

    def parse(self, response):
        for cat in response.xpath("//li[@class='job-category-set-item']"):
            title_node = cat.xpath(".//*[@class='job-category-title']/text()")
            title = title_node.extract()[0].lstrip()
            if title.startswith("Writing"):
                break

            print(title)

            for item in cat.xpath(".//a[@id='job_item']/@href"):
                url = HOST + item.extract() + "1/"
                yield Request(url=url, callback=Main.parse_directory)

    @staticmethod
    def parse_directory(response):
        next_page_node = response.xpath("//link[@rel='next']/@href")
        if next_page_node:
            yield Request(url=next_page_node.extract()[0], callback=Main.parse_directory)

        for link in LinkExtractor(allow=HOST + "/projects/.+/.+/$").extract_links(response):
            project = ProjectItem()
            project["url"] = link.url
            yield project
