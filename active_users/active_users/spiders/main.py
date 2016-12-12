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

        projects = []
        for project in db.new_projects.find():
            projects.append(project["pid"])

        for pid in projects:
            yield Request(self.bids_url + str(pid), callback=self.parse_bids)

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
