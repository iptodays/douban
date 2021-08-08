#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File: douban.py
@Description: 
@Time: 2021/08/08 16:22:48
@Author: iptoday
@Email: wangdong1221@outlook.com
@Version: 1.0.0
'''

import sys
import time
import requests
from scrapy.selector import Selector
import timeit
import re


headers = {
    "Accept": "",
    "User-Agent": "",
    "Cookie": "",
}


def main():
    start = timeit.default_timer()
    args = sys.argv
    if len(args) > 1:
        for i in range(0, len(args)):
            if i > 0:
                if len(args) > 2 and i > 1:
                    print("PLEASE WAIT, GET NEXT MOVE DATA IN 5 SECIONS LATER.")
                    time.sleep(5)
                get_html(args[i])
    else:
        print("END. Not Found DouBan Ids.")
    end = timeit.default_timer()
    print("END %ss" % round((end-start), 2))


# 获取网页内容并解析
def get_html(id):
    url = "https://movie.douban.com/subject/"+id
    print("START GET %s DATA." % url)
    try:
        response = requests.get(url, headers=headers)
        selector = Selector(
            text=Selector(text=response.text).
            css(u'#content').
            extract_first()
        )
        resource_type = "movie"
        if selector.css(u'#season').extract_first() != None:
            resource_type = "tv"
        rating_num = selector.css(u'.rating_num ::text').extract_first()
        if rating_num == None:
            rating_num = 0
        print("RATING NUM: %s" % rating_num)
        h1s = selector.css(u'h1 span::text').extract()
        title = h1s[0]
        year = ""
        if (len(h1s) > 1):
            year = h1s[1]
            year = year.replace("(", "").replace(")", "")
        print("TITLE: %s" % title)
        print("YEAR: %s" % year)
        cover = selector.css(u'#mainpic img::attr(src)').extract_first()
        print("COVER: %s" % cover)
        attrs = selector.css(u'.attrs').extract()
        directors = Selector(text=attrs[0]).css(u'::text').extract()
        directors = ''.join(directors)
        print("DIRECTORS: %s" % directors)
        writers = Selector(text=attrs[1]).css(u'::text').extract()
        writers = ''.join(writers)
        print("WRITERS: %s" % writers)
        actors = Selector(text=attrs[2]).css(u'::text').extract()
        actors = ''.join(actors)
        print("ACTORS: %s" % actors)

        summary = selector.css(u'#link-report span::text').extract()
        summary = ''.join(summary)
        summary = summary.replace(' ', '')
        print("SUMMARY: %s" % summary)

        releases = []
        runtime = ""
        translation = ""
        spans = selector.css(u'span').extract()
        genres = []
        for span in spans:
            ss = Selector(text=span)
            if ss.css(u'::attr(property)').extract_first() == "v:genre":
                genres.append(ss.css(u'::text').extract_first())
            elif ss.css(u'::attr(property)').extract_first() == "v:initialReleaseDate":
                releases.append(ss.css(u'::text').extract_first())
        print("RELEASES: %s" % releases)
        r = re.findall(u"片长:(([\s\S]*?))又名", response.text)
        if r != None and len(r) > 0:
            r = r[0][0]
            r = r.replace("\n", "").replace("  ", "")
            runtime = "".join(Selector(text=r).css(u"::text").extract())
        print("RUNTIME: %s" % runtime)
        r = re.findall(u"又名:(([\s\S]*?))IMDb", response.text)
        if r != None and len(r) > 0:
            r = r[0][0]
            r = r.replace("\n", "").replace("  ", "")
            translation = "".join(Selector(text=r).css(u"::text").extract())

        print("TRANSLATION: %s" % translation)
        print("TRANSLATION: %s" % translation)
        if isinstance(genres, str):
            genres = [genres]
        if isinstance(releases, str):
            releases = [releases]

        data = {
            "id": id,
            "resource_type": resource_type,
            "rating_num": rating_num,
            "title": title,
            "year": year,
            "cover": cover,
            "genres": genres,
            "director": directors,
            "writers": writers,
            "actors": actors,
            "summary": summary,
            "releases": releases,
            "runtime": runtime,
            "translation": translation,
        }
        print("DATA: %s" % data)
    except:
        print("UNKNOW ERROR, PLEASE RETRY")


if __name__ == "__main__":
    main()
