import json
import os
import pickle
import sys
import timeit
from difflib import SequenceMatcher
from os import listdir
from os.path import isfile, join

directory = os.path.dirname(os.path.realpath(__file__)) + "\\"
listofanimes = []

with open(directory + "JSON\\listofanimes.json", "r") as f:
    listofanimes += json.loads(json.load(f))