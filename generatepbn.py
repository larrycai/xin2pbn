#!/usr/bin/env python3
 # -*- coding: utf-8 -*-
import os
import io
import re
import xin2pbn
import sys

# <a href="http://www.xinruibridge.com/....">....</a>
def get_xinruiurl(file):
    urls = []
    with io.open(file, "r", encoding="utf-8") as contents:
        for line in contents:
            #print line
            #print(line.encode("utf-8"))
            #line='<a href="http://www.xinruibridge.com/....">....</a>'
            matched = re.search("a href=\"(http://isoliu.gitlab.io.*)\">(.*)</a>", line,re.UNICODE)
            if matched:
                urls.append(matched.group(1).encode("utf-8"))
    print(urls)
    return urls

dir="pbn"
def check_file(file, idx):
    filename = os.path.splitext(os.path.basename(file))[0]
    urls = get_xinruiurl(file)
    for index, url in enumerate(urls):
        pbn_file="%s/%s-%02d" % (dir,filename, index)
        xin2pbn.xin2pbn(url.decode("utf-8"), pbn_file)

def generate_pbn(html_files):
    for idx, file in enumerate(html_files):
        if file.endswith(".html"):
            check_file(file, idx)
            
if __name__ == '__main__':
    # print(sys.argv)
    if len(sys.argv) > 1:
       generate_pbn(sys.argv[1:])
    else:
        print("generatepbn.py <files contains xinrul>")
