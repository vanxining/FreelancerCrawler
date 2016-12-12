# -*- coding: utf-8 -*-
import json

from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from ..items import ProjectItem


HOST = "https://www.freelancer.com"


class Main(CrawlSpider):
    name = "new_projects"
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
                url = HOST + item.extract()
                yield Request(url=url, callback=Main.parse_directory)

    @staticmethod
    def parse_directory(response):
        next_page_node = response.xpath("//link[@rel='next']/@href")
        if next_page_node:
            yield Request(url=next_page_node.extract()[0], callback=Main.parse_directory)

        beg = response.body.rfind("__export('dataJson', [[")
        if beg == -1:
            return

        beg += 21
        end = response.body.index("]]", beg) + 2
        root = json.loads(response.body[beg:end])

        for project in root:
            item = ProjectItem()
            item["pid"] = project[0]
            item["url"] = HOST + project[21]

            yield item
