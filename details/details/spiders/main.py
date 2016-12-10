
from scrapy.spiders import Spider
from scrapy.http import Request, FormRequest

import pymongo


class Main(Spider):

    name = "details"
    allowed_domains = ["freelancer.com"]

    index = "https://www.freelancer.com/"

    def start_requests(self):
        return Request(self.index, callback=self.login),

    def login(self, response):
        csrf_token = response.xpath("//input[@name='csrf_token']/@value").extract()[0]

        return FormRequest.from_response(
            response,
            formnumber=1,
            formdata={"username": self.settings["USERNAME"],
                      "passwd": self.settings["PASSWORD"],
                      "savelogin": "on",
                      "csrf_token": csrf_token},
            dont_click=True,
            callback=self.check_login_response
        )

    def check_login_response(self, response):
        if "dashboard" in response.url:
            if self.settings["USERNAME"] in response.body:
                self.log("Successfully logged in.")

                client = pymongo.MongoClient(self.settings["MONGO_URI"])
                db = client[self.settings["MONGO_DATABASE"]]

                for project in db.projects.find():
                    if "raw_html" not in project:
                        yield Request(project["url"], callback=self.parse)

    def parse(self, response):
        pass
