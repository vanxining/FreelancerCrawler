# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from ..items import ProjectItem


class Main(CrawlSpider):
    name = "freelancer"
    allowed_domains = ["freelancer.com"]
    start_urls = ["https://www.freelancer.com/job/"]
    link_extractor = {
        "page": LinkExtractor(allow="/bbsdoc,board,\w+\.html$"),
        "page_down": LinkExtractor(allow="/bbsdoc,board,\w+,page,\d+\.html$"),
        "content": LinkExtractor(allow="/bbscon,board,\w+,file,M\.\d+\.A\.html$"),
    }

    def parse(self, response):
        print response
        # for link in self.link_extractor["page"].extract_links(response):
        #     yield Request(url=link.url, callback=self.parse_page)

    # def parse_page(self, response):
    #     for link in self.link_extractor["page_down"].extract_links(response):
    #         yield Request(url=link.url, callback=self.parse_page)

    #     for link in self.link_extractor["content"].extract_links(response):
    #         yield Request(url=link.url, callback=self.parse_content)

    # def parse_content(self, response):
    #     bbsItem_loader = ItemLoader(item=BbsItem(), response=response)
    #     url = str(response.url)
    #     bbsItem_loader.add_value("url", url)
    #     bbsItem_loader.add_xpath("forum", self._x_query["forum"])
    #     bbsItem_loader.add_xpath("poster", self._x_query["poster"])
    #     bbsItem_loader.add_xpath("content", self._x_query["page_content"])
    #
    #     return bbsItem_loader.load_item()