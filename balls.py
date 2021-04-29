import json
import os
import pickle
import sys
import timeit
from difflib import SequenceMatcher
from os import listdir, walk
from os.path import isfile, join
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from time import sleep

directory = os.path.dirname(os.path.realpath(__file__)) + "\\"

# with open(directory + "JSON\\listofanimes.json", "r") as f:
#     listofanimes = json.loads(json.load(f))

# for i in listofanimes:
#     a = i["Members"]
#     a = a.replace('.', '')
#     try:
#         a = int(a)
#         i["Members"] = a
#     except:
#         pass

# with open(directory + "JSON\\listofanimes.json", "w") as f:
#     json.dump(json.dumps(listofanimes), f)

