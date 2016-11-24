
from __future__ import print_function
import sys

import cookielib
from StringIO import StringIO
from urllib import urlencode
import urllib2
import gzip

import json
import time
import random


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def prepare(use_proxy):
    ckp = urllib2.HTTPCookieProcessor(cookielib.CookieJar())

    if use_proxy:
        proxy_handler = urllib2.ProxyHandler({"http": "http://127.0.0.1:8087"})
        opener = urllib2.build_opener(proxy_handler, ckp)
    else:
        null_proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(null_proxy_handler, ckp)

    urllib2.install_opener(opener)


def login():
    pass


_std_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip",
    "Cache-Control": "no-cache",
}


def open_request_and_read(request):
    response = urllib2.urlopen(request)
    if response.info().get("Content-Encoding") == "gzip":
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)

        return f.read()
    else:
        return response.read()


def make_request(method):
    headers = {}
    headers.update(_std_headers)

    url = "http://api.topcoder.com" + method.encode("utf-8")
    request = urllib2.Request(url, headers=headers)

    return request


def guarded_read(method):
    while True:
        try:
            return open_request_and_read(make_request(method))
        except urllib2.HTTPError, e:
            eprint("HTTP Error", e.code, e.msg)
            eprint(e.geturl())
            eprint(e.fp.read())
        except Exception, e:
            eprint(e)

        random_sleep(20)


def simple_read(url):
    return open_request_and_read(urllib2.Request(url, headers=_std_headers))


def random_sleep(base=2):
    time.sleep(base + random.random())
