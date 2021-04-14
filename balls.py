import json
import os
import pickle
import sys
import timeit
from difflib import SequenceMatcher
from os import listdir
from os.path import isfile, join

directory = os.path.dirname(os.path.realpath(__file__)) + "\\"

settings = {"lastanimelist": "Watching", "standardlist": False, "standardlistname": "Seasonal"}

with open(directory + "settings.json", "w") as f:
    json.dump(json.dumps(settings), f)