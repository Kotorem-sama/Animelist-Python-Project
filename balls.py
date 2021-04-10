import json
import os
import pickle

directory = os.path.dirname(os.path.realpath(__file__)) + '\\'

open_file = open(directory + 'Tests/' + 'Listofanimes.pkl', "rb")
listofanimes = pickle.load(open_file)
open_file.close()

# with open(directory + "JSON\\Listofanimes.json", "w") as f:
#     data = json.load(f)
# print(data)

with open(directory + "JSON\\Listofanimes.json", "w") as json_file:
    json.dump(listofanimes, json_file)