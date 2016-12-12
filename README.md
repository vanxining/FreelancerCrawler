FreelancerCrawler
==========

A simple crawler targeting [Freelancer.com](https://www.freelancer.com/job/) based on Scrapy.

## Usage

* Run `new_projects` subproject to crawl the latest opening projects
* Run `active_users` subproject to crawl the currently active users (developers)
* Run `completed` subproject to crawl the projects the active users have won

Command:
`scrapy crawl subproject -s JOBDIR="crawls/subproject"`

Scrapy shell:
`scrapy shell https://www.freelancer.com/job/ -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"`

## Data storage

The data are stored in MongoDB ran in `localhost`. The database will be named `freelancer` with
three collections:

* new_projects: `db.new_projects.createIndex({pid: 1})`
* active_users: `db.active_users.createIndex({uid: 1})`
* projects: `db.projects.createIndex({id: 1})`
