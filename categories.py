
from collections import namedtuple
from bs4 import BeautifulSoup


Technology = namedtuple("Technology", ("name", "url"))
technologies = []

raw = open("categories.htm").read()
soup = BeautifulSoup(raw, "html.parser")

for category in soup.find_all(class_="job-category-set-item"):
    title_node = category.find(class_="job-category-title")
    title = [s for s in title_node.stripped_strings][0]
    if title.startswith("Writing"):
        break

    print title
    print "============="

    for item in category.find_all(class_="job-category-link"):
        name = item.string.strip()
        name = name[:(name.rindex('(') - 1)]
        url = item["href"]

        tech = Technology(name, url)
        technologies.append(tech)

        print name, url
