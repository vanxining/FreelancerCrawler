
from bs4 import BeautifulSoup


raw = open("categories.htm").read()
soup = BeautifulSoup(raw, "lxml")

print len(soup.find_all(class_="job-category-title"))

for category in soup.find_all(class_="job-category-set-item"):
    title_node = category.find(class_="job-category-title")
    title = [s for s in title_node.stripped_strings][0]
    print title
