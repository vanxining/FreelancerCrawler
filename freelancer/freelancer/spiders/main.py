# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from ..items import ProjectItem


HOST = "https://www.freelancer.com"


def get_page_no(url):
    return int(url[(url[:-1].rindex('/') + 1):-1])


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
        if get_page_no(response.url) == 1:
            last_page_node = response.xpath("//span[@id='project_table_last']/a/@href")
            if len(last_page_node) == 1:
                last = get_page_no(last_page_node.extract()[0])
                chunk = response.url[:-3]

                for i in xrange(2, last + 1):
                    yield Request(url=chunk + "/%d/" % i, callback=Main.parse_directory)

        for link in LinkExtractor(allow=HOST + "/projects/.+/.+/$").extract_links(response):
            print link.url
