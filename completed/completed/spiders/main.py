import json
import pymongo
from scrapy.http import Request
from scrapy.spiders import Spider
from urllib import urlencode
from urlparse import parse_qs


class Main(Spider):

    name = "completed"
    allowed_domains = ["freelancer.com"]

    reviews_url = "https://www.freelancer.com/api/projects/0.1/reviews/?"
    params = {
        "to_users[]": -1,
        "offset": 0,
        "limit": 10,
        "compact": "true",
        "contest_details": "true",
        "contest_job_details": "true",
        "project_details": "true",
        "project_job_details": "true",
        "role": "freelancer",
        "user_avatar": "true",
        "user_country_details": "true",
        "user_details": "true",
        "review_types[]": "project",
    }
    params2 = {
        "review_types[]": "contest",
    }

    bids_url = "https://www.freelancer.com/ajax/project/getBids.php?project_id="

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.client = None
        self.db = None

    def start_requests(self):
        self.client = pymongo.MongoClient(self.settings["MONGO_URI"])
        self.db = self.client[self.settings["MONGO_DATABASE"]]

        users = []
        for user in self.db.active_users.find():
            users.append(user["uid"])

        for user in users:
            Main.params["to_users[]"] = user
            Main.params["offset"] = 0
            pstr = urlencode(Main.params) + '&' + urlencode(Main.params2)

            yield Request(Main.reviews_url + pstr, callback=self.parse_reviews)

    def parse_reviews(self, response):
        root = json.loads(response.body)
        if u"projects" not in root[u"result"]:
            return

        params = parse_qs(response.url)
        Main.params["to_users[]"] = params["to_users[]"][0]
        Main.params["offset"] = int(params["offset"][0]) + int(params["limit"][0])
        pstr = urlencode(Main.params) + '&' + urlencode(Main.params2)

        yield Request(Main.reviews_url + pstr, callback=self.parse_reviews)

        for project in root[u"result"][u"projects"].itervalues():
            pid = project[u"id"]

            if not self.db.projects.find_one({u"id": pid}):
                self.db.projects.insert(project)

                yield Request(self.bids_url + str(pid), callback=self.parse_bids)

    def parse_bids(self, response):
        root = json.loads(response.body)
        del root[u"status"]

        pid = int(response.url[(response.url.rfind('=') + 1):])
        project = self.db.projects.find_one({u"id": pid})
        project[u"result"] = root

        self.db.projects.update({u"id": pid}, {u"$set": project})

    def parse(self, response):
        pass
