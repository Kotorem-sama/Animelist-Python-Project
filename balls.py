import json
import os
import pickle
import sys
import timeit
from difflib import SequenceMatcher
from os import listdir
from os.path import isfile, join
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from time import sleep

directory = os.path.dirname(os.path.realpath(__file__)) + "\\"
listofanimes = []
lis = []

with open(directory + "JSON\\listofanimes.json", "r") as f:
    listofanimes += json.loads(json.load(f))

lists = [f for f in listdir(directory + "JSON\\Lists") if isfile(join(directory + "JSON\\Lists", f))]
for i in lists:
    with open(directory + "JSON\\Lists\\" + i, "r") as f:
        lis2 = json.loads(json.load(f))
        for l in lis2:
            l["List"] = i.replace(".json", "")
        lis += lis2

def page_soupgetter(URL):
    try:
        with uReq(URL) as uClient:
            page_html = uClient.read()
        page_soup = soup(page_html, "html.parser")
    except:
        page_soup = soup()
    return page_soup

def infolist(myanimelistpage, data2):
    list2 = myanimelistpage.find('span', text=data2).find_previous('div').find_all('a')
    list1 = []
    for i in list2:
        list1.append(i.text)
    return list1

def infotext(myanimelistpage, data2):
    text = myanimelistpage.find('span', text=data2).find_previous('div').text
    return text.replace(data2, '').strip()

def getlastdata(index):
    URL = 'https://myanimelist.net/anime/' + listofanimes[index]["Anime ID"]
    myanimelistpage = page_soupgetter(URL)
    listofanimes[index]["Studios"] = infolist(myanimelistpage, "Studios:")
    listofanimes[index]["Licensors"] = infolist(myanimelistpage, "Licensors:")
    listofanimes[index]["Producers"] = infolist(myanimelistpage, "Producers:")
    listofanimes[index]["Source"] = infotext(myanimelistpage, "Source:")
    listofanimes[index]["Score"] = myanimelistpage.find('span', text="Score:").find_next('span').text
    listofanimes[index]["Members"] = infotext(myanimelistpage, "Members:")

for j in lis:
    j["Watched"] = 0
    j["Watched Episodes"] = 0
    j["Rating"] = None
    print(j)

lis.append({"List": "Watching"})
lis.append({"List": "Completed"})
lis.append({"List": "On Hold"})
lis.append({"List": "Dropped"})

lists = []

for m in lis:
    if m["List"] not in lists:
        lists.append(m["List"])

with open(directory + "JSON\\lists.json", "w") as f:
    json.dump(json.dumps(lis), f)