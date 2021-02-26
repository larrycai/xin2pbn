#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
import re
import sys
import json
import pkgutil

from urllib.parse import urlparse
from string import Template
import urllib.parse
from collections import deque

url="http://www.xinruibridge.com/deallog/DealLog.html?bidlog=P%3B1N,P,4D,P%3B4H,P,4N,P%3B5H,P,5N,P%3B6C,P,6D,P%3B7H,P,P,P%3B&playlog=W:2H,5H,3H,9H%3BS:KC,8C,2C,4C%3BS:5C,JC,AC,3C%3BN:6C,9C,AH,QC%3BS:3D,8D,AD,2D%3BN:KH,3S,4D,4H%3BN:QH,8S,4S,8H%3BN:JH,9S,6D,TH%3BN:7H,5D,5S,7D%3BN:6H,TS,JD,TD%3BN:JS,QS,KS,2S%3BS:&deal=QT983.3.Q52.T943%20AK654.A9.J643.K5%2072.T842.KT87.QJ8%20J.KQJ765.A9.A762&vul=EW&dealer=E&contract=7H&declarer=S&wintrick=13&score=1510&str=%E9%94%A6%E6%A0%87%E8%B5%9B%20%E7%AC%AC1%E8%BD%AE%20%E7%89%8C%E5%8F%B7%206/8&dealid=440219531&pbnid=133129440"

dir="."
PBN_FILE="output"

DECLARE2LEADER={"E":"S","S":"W","W":"N","N":"E"," ":" "}
def bidlog2auction(bidlog):
# 'P;1N,P,4D,P;4H,P,4N,P;5H,P,5N,P;6C,P,6D,P;7H,P,P,P;'
    str = bidlog.replace(","," ") \
        .replace(";"," ").replace("P","Pass"). \
        replace("N","NT")
    abc = str.split(" ")
    auction=""
    for i in range(0, len(abc), 4):
        auction = auction + " ".join(abc[i:i+4]) + "\n"
    return(auction.rstrip())

seq_map={"E":0, "S":1, "W": 2,"N": 3,}
def save_hands(line):
    ## save 4 hands cards into E-S-W-N
    direct = line[0]
    cards=line[2:].split(",")
    hands = deque(cards)
    shift=seq_map[direct]
    hands.rotate(shift)
    # print("after shift:", hands)
    return hands

def show_play(leader, line):
    # print(line)
    cards=save_hands(line)
    shift=seq_map[leader]
    cards.rotate(-shift)
    #print(new_cards)
    cards =[ x[1]+x[0] for x in cards if len(x)==2]
    # print("new:", cards)
    return " ".join(cards)
    #if check_seq:
        
def playlog2play(playlog):
# playlog=W:2H,5H,3H,9H;S:KC,8C,2C,4C;S:5C,JC,AC,3C;N:6C,9C,AH,QC;
    plays=playlog.split(";")
    leader=plays[0][0]
    play=""
    for round in plays:
        if len(round)>1:
            play = play + show_play(leader,round) + "\n"
    return play

def fixcontract(contract):
# 3NX => 3NTX for PBNJview
    return contract.replace("N","NT")

def xin2pbn(src_url, output):
    #print("wahtttttttt")
    #print(url)
    url = src_url.replace("&amp;","&").replace(";","%3B")
    o = urlparse(url)
    all = urllib.parse.parse_qs(o.query)
    #print(all)
    for k in all:
        all[k] = all[k][0]
    #print(all)
    all["leader"] = DECLARE2LEADER[all["declarer"]]
    all["auction"] = bidlog2auction(all["bidlog"])
    if "playlog" in all:
        all["play"] = playlog2play(all["playlog"])
    else:
        all["play"] = ""
    all["contract"] = fixcontract(all["contract"])
    template = pkgutil.get_data(__name__,'template.pbn')
    #with open('template.pbn') as filein:
    #    src = Template(filein.read())
    src = Template(template.decode('utf-8'))
    result = src.safe_substitute(all)
    output = output + ".pbn"
    with io.open(output, "w", encoding="utf-8") as text_file:
        print("write to file %s" % output)
        text_file.write(result)

# <a href="http://www.xinruibridge.com/....">....</a>
def get_xinruiurl(file):
    urls = []
    with io.open(file, "r", encoding="utf-8") as contents:
        for line in contents:
            #print line
            #print(line.encode("utf-8"))
            #line='<a href="http://www.xinruibridge.com/deallog/DealLog.html....">....</a>'
            # print(line)
            matched = re.search("href=\"(http.*DealLog.*)\">(.*)</a>", line,re.UNICODE)
            if matched:
                urls.append(matched.group(1).encode("utf-8"))
    print(urls)
    return urls

def check_file(file):
    filename = os.path.splitext(os.path.basename(file))[0]
    urls = get_xinruiurl(file)
    for index, url in enumerate(urls):
        pbn_file="%s/%s-%02d" % (dir,filename, index + 1)
        xin2pbn(url.decode("utf-8"), pbn_file)

def generate_pbn_from_html(html_files):
    for file in html_files:
        if file.endswith(".html") or file.endswith(".htm"):
            check_file(file)

def main():
    # print(sys.argv)
    if len(sys.argv) > 1:
        param = sys.argv[1:]
        if param[0].startswith("http"):
            xin2pbn(param[0], PBN_FILE)
        else:
            generate_pbn_from_html(param)
    else:
        print("xin2pbn.py <url>|<html>")

if __name__ == '__main__':
    main()
