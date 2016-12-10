import json
import pymongo
from scrapy.http import Request
from scrapy.spiders import Spider
from ..items import ActiveUserItem


class Main(Spider):

    name = "active_users"
    allowed_domains = ["freelancer.com"]

    index = "https://www.freelancer.com/"
    bids_url = "https://www.freelancer.com/ajax/project/getBids.php?project_id="

    def start_requests(self):
        client = pymongo.MongoClient(self.settings["MONGO_URI"])
        db = client[self.settings["MONGO_DATABASE"]]

        for project in db.projects.find():
            url = project["url"]
            pos = url.rfind('-')
            if pos != -1:
                pid = url[(pos + 1):-1]
                if len(pid) == 8 and pid.isdigit():
                    yield Request(self.bids_url + pid, callback=self.parse_bids)
                    continue

            yield Request(url, callback=self.parse_project)

    def parse_project(self, response):
        url_node = response.xpath("//meta[@property='al:ios:url']/@content")
        url = url_node.extract()[0]
        pid = url[(url.rindex('/') + 1):]

        yield Request(self.bids_url + pid, callback=self.parse_bids)

    @staticmethod
    def parse_bids(response):
        root = json.loads(response.body)

        for bid in root["bids"]:
            user_url = bid["user"]["url"]
            nname = user_url[(user_url.rindex('/') + 1):user_url.rindex('.')]

            user = ActiveUserItem()
            user["uid"] = int(bid["user"]["id"])
            user["nname"] = nname

            yield user

    def parse(self, response):
        pass
