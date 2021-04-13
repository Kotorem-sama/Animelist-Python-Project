import json
import os
import pickle
import sys
import timeit

directory = os.path.dirname(os.path.realpath(__file__)) + '\\'
def test1():
    with open(directory + 'Tests/' + 'Listofanimes.pkl', "rb") as L:
        listofanimes = pickle.load(L)

# # split listofanimes in seperate lists and converting them to json string
# list1 = listofanimes[0:10000]
# list1 = json.dumps(list1)
# list2 = listofanimes[10000:20000]
# list2 = json.dumps(list2)
# list3 = listofanimes[20000:-1]
# list3.append(listofanimes[-1])
# list3 = json.dumps(list3)

# with open(directory + "JSON\\Listofanimes1.json", "w") as f:
#     json.dump(list1, f)

# with open(directory + "JSON\\Listofanimes2.json", "w") as f:
#     json.dump(list2, f)

# with open(directory + "JSON\\Listofanimes3.json", "w") as f:
#     json.dump(list3, f)

def test2():
    check = ["Listofanimes1.json", "Listofanimes2.json", "Listofanimes3.json"]
    fulllist1234 = []
    for i in check:
        with open(directory + "JSON\\" + i, "r") as f:
            fulllist1234 += json.loads(json.load(f))