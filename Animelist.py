import json
from random import choice
from operator import itemgetter
from difflib import SequenceMatcher
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests as req
import time
import random
import urllib
from http.cookiejar import CookieJar
from os import listdir, remove, rename, mkdir, walk
from os.path import isfile, join, dirname, realpath

directory = dirname(realpath(__file__)) + '\\'
lists = []
settings = None
list_name = None
animelist = []
listofanimes = []
emptyanimelist = [{"List": "Watching"}, {"List": "Completed"}, {"List": "On Hold"}, {"List": "Dropped"}, {"List": "Plan to Watch"}]
emptysettings = {"lastanimelist": "Watching", "standardlist": False, "standardlistname": "Watching", "sorting": "Anime"}
newfile = False

# New function to load json files.
def newload(directory2):
    with open(directory2, "r") as f:
        loading = json.loads(json.load(f))
    return loading

# New function to save json files.
def newsave(directory2, itemtosave):
    with open(directory2, "w") as f:
        json.dump(json.dumps(itemtosave), f)

# Will make it possible to use the project even if you don't have the other files such as settings and an animelist.
def filedoesnotexistfix(filename, folderdirectory, emptystate):
    global newfile
    try:
        data = newload(folderdirectory + "\\" + filename)
    except:
        try:
            mkdir(folderdirectory)
            newsave(folderdirectory + "\\" + filename, emptystate)
            data = emptystate
            if filename == "lists.json":
                newfile = True
        except:
            newsave(folderdirectory + "\\" + filename, emptystate)
            data = emptystate
            if filename == "lists.json":
                newfile = True
    return data

# Loads the first bits.
def start():
    global lists, settings, list_name, listofanimes, animelist, newfile
    settings = filedoesnotexistfix("settings.json", directory + "JSON", emptysettings)
    listofanimes = newload(directory + "JSON\\listofanimes.json")
    animelist = filedoesnotexistfix("lists.json", directory + "JSON", emptyanimelist)
    lists = []
    for m in animelist:
        if m["List"] not in lists:
            lists.append(m["List"])
    if newfile:
        settings["lastanimelist"] = lists[0]
        settings["standardlistname"] = lists[0]
        newsave(directory + "JSON\\settings.json", settings)
        list_name = lists[0]
        newfile = False
    else:
        if settings["standardlist"] == True:
            list_name = settings["standardlistname"]
        else:
            list_name = settings["lastanimelist"]
    print(f"You are currently viewing '{list_name}'")

header = {
    'host': 'crunchyroll.com',
    'referer': 'https://www.google.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
}

# Returns a list of anime names that now have the same length as the input.
def lengthmaker(checklist, length):
    checklist2 = []
    for i in checklist:
        newword = i.ljust(length, ' ')
        newword = newword[0:length]
        checklist2.append(newword)
    return checklist2

# Returns a list for the similarity check with anime names.
def checklistmaker(i, chosenlist4):
    checklist = []
    try:
        checklist = [chosenlist4[i]["Anime"]]
    except:
        pass
    try:
        if chosenlist4[i]["English"] != '':
            checklist.append(chosenlist4[i]["English"])
    except:
        pass
    try:
        if chosenlist4[i]["Synonyms"] != []:
            for yikerss in chosenlist4[i]["Synonyms"]:
                checklist.append(yikerss)
    except:
        pass
    return checklist

# Returns the anime that resembles the input the most.
def maximumsimilarity(a, chosenlist2):
    maximum = 50
    maximumanimelist = []
    a = a.lower()
    for i in range(0, len(chosenlist2)):
        checklist = lengthmaker(checklistmaker(i, chosenlist2), len(a))
        for j in checklist:
            b = j.lower()
            sim = similarity(b, a)
            if sim > maximum:
                maximum = sim
                maximumanimelist = [i]
            elif sim == maximum and i not in maximumanimelist:
                maximumanimelist.append(i)
    return maximumanimelist

# Returns the HTML of a website or if it doesn't exist it just returns soup
def page_soupgetter(URL):
    with uReq(URL) as uClient:
        page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")
    return page_soup

# Returns the given namelist, but it's now URL ready
def namelistmaker(namelist, changelist):
    namelist2 = []
    for name in namelist:
        name = name.lower()
        for i in range(0, len(changelist)):
            if i % 2:
                pass
            else:
                name = name.replace(changelist[i], changelist[i+1])
        name = name.strip().replace(' ', '-')
        if name[-1] == '-' and name[-2] != '-':
            name = name[0:-1]
        if name[0] == '-':
            name = name[1:-1] + name[-1]
        name = name.replace('---', '-').replace('--', '-')
        if not name in namelist2:
            namelist2.append(name)
    return namelist2

# Checks if a given link exists
def Linkchecker(Cleanlink, name, header=header):
    attempt = Cleanlink + name
    r = req.get(attempt, timeout=20, headers=header)
    if r.status_code == 200:
        return r.url

# Returns the first link that exists or 'Not Found...' if it doesn't exist. In that case I will try to find an accessible website where you can watch it.
def wheretowatch(namelist, year = None, Producers = []):
    links = ["https://gogoanime.ai/category/", "https://www2.kickassanime.rs/anime/", "https://kissanime.ru.com/series/", "https://www1.animeshow.tv/", "https://www.animefreak.tv/watch/"]
    forbidden = [None, "https://www2.kickassanime.rs/", "https://www2.kickassanime.rs/anime/", "https://www1.animeshow.tv"]
    aa = ["ä", "a", "é", "e", "à", "a", "ö", "o", "â", "a", "ü", "u", "◯", "o", "ē", "e", "○", "o", "ù", "u", "x", "x", "ð", "d", "ū", "u", "á", "a", "Ω", "w", "ì", "i", "ž", "z", "ò", "o", "ó", "o", "ǔ", "u", "ô", "o", "½", "12", "+", "", "&", "", "⅙", "16", "Δ", "d", "³", "3", "Ψ", "ps", "∞", "", "√", "d", "★", "", ".", "-", ":", "", "/", "", ";", "", "♥", "-", "@", "", "☆", "-", "*", "-", "∽", "-", "=", "-", "_", "-", "†", "-", "―", "-", "～", "-", "!", "", "(", "", ")", "", "?", "", "'", "", ",", "", "%", "", "♡", "", "²", "", '"', "", "#", "", "$", "", "♪", "", "^", "", "♭", "", "[", "", "]", "", ">", "", "␣", "", "…", "", "→", "", "←", "", "◎", "", "μ", "", "°", "", "＊", "", "“", "", "♂", "", "△", "", "￥", "", "＿", "", "’", "", "・", "", "『", "", "』", "", "＋", "", "♀", "", "！", ""]
    bb = ["(tv)", "", "ä", "a", "é", "e", "à", "a", "ö", "o", "â", "a", "ü", "u", "◯", "o", "ē", "e", "○", "o", "ù", "u", "x", "x", "ð", "d", "ū", "u", "á", "a", "Ω", "w", "ì", "i", "ž", "z", "ò", "o", "ó", "o", "ǔ", "u", "ô", "o", "½", "12", "+", "", "&", "", "⅙", "16", "Δ", "d", "³", "3", "Ψ", "", "∞", "", "√", "d", "★", "", ".", "", ":", "", "/", "", ";", "", "♥", "", "@", "-", "☆", "-", "*", "-", "∽", "-", "=", "-", "_", "-", "†", "-", "―", "-", "～", "-", "!", "", "(", "", ")", "", "?", "", "'", "", ",", "", "%", "", "♡", "", "²", "", '"', "", "#", "", "$", "", "♪", "", "^", "", "♭", "", "[", "", "]", "", ">", "", "␣", "", "…", "", "→", "", "←", "", "◎", "", "μ", "", "°", "", "＊", "", "“", "", "♂", "", "△", "", "￥", "", "＿", "", "’", "", "・", "", "『", "", "』", "", "＋", "", "♀", "", "！", ""]
    cc = ["(tv)", "", "ä", "a", "é", "e", "à", "a", "ö", "o", "â", "a", "ü", "u", "◯", "o", "ē", "e", "○", "o", "ù", "u", "x", "x", "ð", "d", "ū", "u", "á", "a", "Ω", "w", "ì", "i", "ž", "z", "ò", "o", "ó", "o", "ǔ", "u", "ô", "o", "+", "", "&", "", "⅙", "16", "Δ", "", "³", "", "Ψ", "", "√", "", "★", "", ".", "-", ":", "", "/", "-", ";", "", "♥", "", "@", "", "☆", "-", "*", "-", "∽", "-", "=", "-", "_", "-", "†", "-", "―", "-", "～", "-", "!", "", "(", "", ")", "", "?", "", "'", "", ",", "", "%", "", "♡", "", "²", "", '"', "", "#", "", "$", "", "♪", "", "^", "", "♭", "", "[", "", "]", "", ">", "", "␣", "", "…", "", "→", "", "←", "", "◎", "", "μ", "", "°", "", "＊", "", "“", "", "♂", "", "△", "", "￥", "", "＿", "", "’", "", "・", "", "『", "", "』", "", "＋", "", "♀", "", "！", ""]
    dd = ["ä", "a", "é", "e", "à", "a", "ö", "o", "â", "a", "ü", "u", "◯", "o", "ē", "e", "○", "o", "ù", "u", "x", "x", "ð", "d", "ū", "u", "á", "a", "Ω", "w", "ì", "i", "ž", "z", "ò", "o", "ó", "o", "ǔ", "u", "ô", "o", "½", "", "+", "plus", "&", "and", "⅙", "16", "Δ", "", "³", "", "Ψ", "", "∞", "", "√", "", "★", "-", ".", "-", ":", "-", "/", "-", ";", "-", "♥", "", "@", "", "☆", "-", "*", "-", "∽", "-", "=", "-", "_", "-", "†", "-", "―", "-", "～", "-", "!", "", "(", "", ")", "", "?", "", "'", "", ",", "", "%", "", "♡", "", "²", "", '"', "", "#", "", "$", "", "♪", "", "^", "", "♭", "", "[", "", "]", "", ">", "", "␣", "", "…", "", "→", "", "←", "", "◎", "", "μ", "", "°", "", "＊", "", "“", "", "♂", "", "△", "", "￥", "", "＿", "", "’", "", "・", "", "『", "", "』", "", "＋", "", "♀", "", "！", ""]
    ee = ["ä", "a", "é", "", "à", "a", "ö", "o", "â", "a", "ü", "u", "◯", "o", "ē", "e", "○", "o", "ù", "u", "x", "x", "ð", "d", "ū", "u", "á", "a", "Ω", "w", "ì", "i", "ž", "z", "ò", "o", "ó", "o", "ǔ", "u", "ô", "o", "½", "", "+", "", "&", "", "⅙", "16", "Δ", "", "³", "", "Ψ", "", "∞", "", "√", "", "★", "", ".", "", ":", "", "/", "", ";", "", "♥", "", "@", "", "☆", "-", "*", "-", "∽", "-", "=", "-", "_", "-", "†", "-", "―", "-", "～", "-", "!", "", "(", "", ")", "", "?", "", "'", "", ",", "", "%", "", "♡", "", "²", "", '"', "", "#", "", "$", "", "♪", "", "^", "", "♭", "", "[", "", "]", "", ">", "", "␣", "", "…", "", "→", "", "←", "", "◎", "", "μ", "", "°", "", "＊", "", "“", "", "♂", "", "△", "", "￥", "", "＿", "", "’", "", "・", "", "『", "", "』", "", "＋", "", "♀", "", "！", ""]
    no = [aa, bb, cc, dd, ee]

    if "Anime Beans" in Producers:
        return "https://apps.qoo-app.com/en/app/7228"

    for j in range(0, len(links)):
        namelist2 = namelistmaker(namelist, no[j])
        for i in namelist2:
            yikers = Linkchecker(links[j], i, None)
            if yikers not in forbidden:
                return yikers

        # # Animetake Checker
        # yikers = Linkchecker("https://animetake.tv/anime/", i, {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'})
        # if yikers != None:
        #     return yikers

        # # Animefrenzy Checker
        # yikers = Linkchecker("https://animefrenzy.org/anime/", i, None)
        # if yikers != None:
        #     return yikers

    return 'Not Found...'

def changes(b, myanimelistpage):
    if listofanimes[b]['Episodes'] == "Unknown":
        listofanimes[b]['Episodes'] = infotext(myanimelistpage, 'Episodes:')
    if listofanimes[b]['Aired'] == "Not available" or listofanimes[b]['Aired'][-1] == "?":
        try:
            listofanimes[b]['Aired'] = infotext(myanimelistpage, 'Premiered:')
        except:
            listofanimes[b]['Aired'] = infotext(myanimelistpage, 'Aired:')
    if listofanimes[b]['Duration'] == "Unknown":
        listofanimes[b]['Duration'] = infotext(myanimelistpage, 'Duration:')
    listofanimes[b]["Score"] = myanimelistpage.find('span', text="Score:").find_next('span').text

def whichanime(a, chosenlist3):
    if a.lower() == 'stop' or a.lower() == 'end' or a.lower() == 'cancel':
        return None
    outcome = maximumsimilarity(a, chosenlist3)
    if len(outcome) == 1:
        b = int(outcome[0])
    elif len(outcome) == 0:
        print("You really need to learn how to type")
        return None
    else:
        for i in range(0, len(outcome)):
            try:
                print(f"{i + 1}. {chosenlist3[outcome[i]]['Anime']} (English: {chosenlist3[outcome[i]]['English']}) (Type: {chosenlist3[outcome[i]]['Type']})")
            except:
                print(f"{i + 1}. {chosenlist3[outcome[i]]['Anime']}")
        d = input('Which anime do you wish to know more about? (number/stop): ')
        try:
            d = int(d)
            b = int(outcome[d - 1])
        except:
            print('Process Cancelled')
            return None
    return b

def infolist(myanimelistpage, data2):
    list2 = myanimelistpage.find('span', text=data2).find_previous('div').find_all('a')
    list1 = []
    for i in list2:
        list1.append(i.text)
    return list1

def infotext(myanimelistpage, data2):
    text = myanimelistpage.find('span', text=data2).find_previous('div').text
    return text.replace(data2, '').strip()

def getlastdata(index, myanimelistpage):
    listofanimes[index]["Studios"] = infolist(myanimelistpage, "Studios:")
    listofanimes[index]["Licensors"] = infolist(myanimelistpage, "Licensors:")
    listofanimes[index]["Producers"] = infolist(myanimelistpage, "Producers:")
    listofanimes[index]["Source"] = infotext(myanimelistpage, "Source:")
    listofanimes[index]["Score"] = myanimelistpage.find('span', text="Score:").find_next('span').text
    listofanimes[index]["Members"] = infotext(myanimelistpage, "Members:")

def search():
    b = whichanime(input("Which anime are you looking for?: "), listofanimes)
    if b == None:
        pass
    else:
        URL = 'https://myanimelist.net/anime/' + listofanimes[b]["Anime ID"]
        try:
            myanimelistpage = page_soupgetter(URL)
            if listofanimes[b]["Score"] == "":
                getlastdata(b, myanimelistpage)
            else:
                changes(b, myanimelistpage)
        except:
            print("Myanimelist page does not exist anymore.")
        a = listofanimes[b]
        for yi in a:
            key = yi
            value = a[yi]
            if value == "" or value == []:
                pass
            else:
                if type(value) == list:
                    value2 = value.pop(0)
                    if value != []:
                        for listitem in value:
                            value2 += ', ' + listitem
                else:
                    value2 = value
                spaces = (19 - len(key)) * " "
                print(key + ':' + spaces + value2)
        print(f"Where to watch:     {wheretowatch(checklistmaker(b, listofanimes), None)}")

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio() * 100

def load(file_name):
    global animelist, settings, list_name
    settings["lastanimelist"] = file_name
    newsave(directory + "JSON\\settings.json", settings)
    list_name = file_name

def addlist():
    global lists, directory, animelist
    listname = ''
    a = input('What will be the name of the new list?: ')
    if a.lower() == 'stop' or a.lower() == 'end' or a.lower() == 'cancel':
        pass
    elif a in lists:
        b = input("This name is already taken. Do you want to call this list '" + a + " 2'?: ")
        if b.lower() == 'yes':
            listname = a + ' 2'
        else:
            addlist()
    else:
        listname = a
    if listname != '' or listname != " ":
        lists.append(listname)
        animelist.append({"List": listname})
        newsave(directory + "JSON\\lists.json", animelist)
        c = input('Do you want to load ' + listname + '?: ')
        if c.lower() == 'yes':
            load(listname)

def actualdeletelist(name):
    global animelist
    for i in animelist:
        if i["List"] == name:
            animelist.remove(i)
    newsave(directory + "JSON\\lists.json", animelist)

def deletelist():
    global lists
    print(lists)
    a = input('Which list do you want to delete?: ')
    name = whichlist(a)
    if name != None:
        b = input("Are you sure you want to delete '" + name + "'? (yes/no): ")
        if b.lower() == 'yes':
            lists.remove(name)
            actualdeletelist(name)
            if list_name == name:
                print(lists)
                c = input('Which list do you want to load?: ')
                b = whichlist(c)
                if b == None:
                    return
                load(b)
                print("Loaded list '" + b + "'")

def actualaddanime(newanime, c, list_name2):
    global animelist
    newanime["Index"] = c
    newanime["Anime"] = listofanimes[c]["Anime"]
    inlist = False
    for l in range(0, len(animelist)):
        try:
            if animelist[l]["Index"] == c:
                inlist = True
                inlistname = l
                inlistactualname = animelist[l]["List"]
        except:
            pass
    if inlist:
        if inlistname == list_name2:
            print("Anime already in animelist")
        else:
            changelist = input(f"This anime {newanime['Anime']} already exists in {inlistactualname}. Do you want to add it to {list_name2}? (yes/no): ")
            if changelist.lower() == "yes":
                changewhichlist(inlistname, list_name2)
    else:
        b = input("Are you sure you want to add '" + listofanimes[c]["Anime"] + "'?: ")
        if b.lower() == 'yes' or b == '':
            animelist.append(newanime)
            newsave(directory + "JSON\\lists.json", animelist)

def changewhichlist(index, listnametochangeto):
    global animelist
    animelist[index]["List"] = listnametochangeto
    newsave(directory + "JSON\\lists.json", animelist)

def add(wayf):
    global animelist, list_name
    newanime = {"Index": "", "Anime": "", "List": list_name, "Watched": 0, "Watched Episodes": 0, "Rating": None}
    if wayf == 'Anime ID':
        c = ''
        a = input("What is the Anime ID?: ")
        if a.lower() == 'stop' or a.lower() == 'end' or a.lower() == 'cancel':
            return
        else:
            for i in range(0, len(listofanimes)):
                if str(listofanimes[i]["Anime ID"]) == str(a):
                    c = i
            if c == '':
                print('This Anime ID does not exist.')
                add(wayf)
            else:
                actualaddanime(newanime, c, list_name)
                add(wayf)
    elif wayf == 'Anime':
        a = whichanime(input("Which anime do you want to add?: "), listofanimes)
        if a == None:
            pass
        else:
            actualaddanime(newanime, a, list_name)
            add(wayf)
    sort2()

def delete():
    global animelist
    b = ''
    a = input('Which anime do you want to remove from the list: ')
    if a.lower() == 'stop' or a.lower() == 'end' or a.lower() == 'cancel':
        pass
    elif a.lower() == 'help' or a.lower() == 'print':
        printanimelist()
        delete()
    else:
        for i in animelist:
            try:
                if i["Anime"] == a:
                    b = input("Are you sure you want to delete '" + i["Anime"] + "'?: ")
                    if b.lower() == 'yes' or b == '':
                        animelist.remove(i)
                        newsave(directory + "JSON\\lists.json", animelist)
                        break
            except:
                pass
        if b != '':
            print('This anime does not exist in this list.')
        delete()
    sort2()

def whichlist(b):
    if b.lower() == 'stop' or b.lower() == 'end' or b.lower() == 'cancel':
        return None
    else:
        while b not in lists:
            b = input('This list does not exist. Try again: ')
    return b

def loadlist():
    print(lists)
    a = input('Which list do you want to access?: ')
    b = whichlist(a)
    if b == None:
        return
    load(b)
    print(f"You are currently viewing '{list_name}'")

def sort2():
    global animelist
    sortmode = settings["sorting"]
    reverse = False
    if sortmode == "Score":
        reverse = True
    for i in animelist:
        try:
            useless = i["Anime"]
            useless = useless
            checkforsortpossibility = i
            break
        except:
            pass
    if sortmode not in checkforsortpossibility:
        for j in animelist:
            try:
                j[sortmode] = listofanimes[j["Index"]][sortmode]
            except:
                pass
    newanimelist = []
    empties = []
    for item in animelist:
        try:
            useless = item["Anime"]
            useless = useless
            newanimelist.append(item)
        except:
            empties.append(item)
    animelist = sorted(newanimelist, key = lambda i: i[sortmode], reverse=reverse) + empties
    newsave(directory + "JSON\\lists.json", animelist)

def changelistname():
    print(lists)
    z = input('The name of which list do you want to change?: ')
    name = whichlist(z)
    if name == None:
        return
    newname = input("What will the new name of the list be?: ")
    changename(name, newname)

def printanimelist():
    a = 1
    global animelist, list_name
    for i in animelist:
        try:
            if i["List"] == list_name:
                if settings['sorting'] == "Anime":
                    print(f"{str(a)}. {i['Anime']}")
                else:
                    print(f"{str(a)}. {i['Anime']} {settings['sorting']}: {i[settings['sorting']]}")
                a += 1
        except:
            pass

def randomanime():
    global animelist
    choicelist = []
    for i in animelist:
        try:
            if i["List"] == list_name:
                useless = i["Anime"]
                useless = useless
                choicelist.append(i)
        except:
            pass
    print(choice(choicelist)["Anime"])

def trueorfalsesetting(a):
    global settings
    b = input("True or False?: ")
    if b.lower() == 'stop' or b.lower() == 'end':
        pass
    elif b.lower() == "true":
        settings[a] = True
    elif b.lower() == "false":
        settings[a] = False
    else:
        trueorfalsesetting(a)

def listsetting(a):
    global settings
    print(lists)
    b = input('Which list do you want this setting to change to?: ')
    chosenlist = whichlist(b)
    if chosenlist == None:
        return
    settings[a] = chosenlist

def changesortingmethod():
    global settings
    choiceslist = ["Anime", "English", "Anime ID", "Type", "Episodes", "Aired", "Rating", "ActualDuration", "Source", "Score", "Members", "Watched", "Watched Episodes", "Rating"]
    print(choiceslist)
    chosensortmethod = input("Which sorting method do you want to use?: ")
    while chosensortmethod not in choiceslist:
        chosensortmethod = input("This sorting method does not exist. Try again: ")
    settings["sorting"] = chosensortmethod
    sort2()

def whichsetting():
    a = input("Which setting do you want to change?: ")
    if a.lower() == 'stop' or a.lower() == 'end':
        pass
    else:
        while a.lower() not in settings:
            a = input("This setting does not exist. Try again: ")
        if type(settings[a]) == bool:
            trueorfalsesetting(a)
        elif a.lower() == "lastanimelist" or a.lower() == "standardlistname":
            listsetting(a)
        elif a.lower() == "sorting":
            changesortingmethod()

def changename(listname, newlistname):
    global lists, animelist
    lists.remove(listname)
    lists.append(newlistname)
    for i in animelist:
        if i["List"] == listname:
            i["List"] = newlistname
    newsave(directory + "JSON\\lists.json", animelist)
    if listname == list_name:
        load(newlistname)

def setting():
    global settings
    for i in settings:
        spaces = (19 - len(i)) * " "
        print(f"{i}:{spaces}{settings[i]}")
    whichsetting()
    newsave(directory + "JSON\\settings.json", settings)
    start()

def makeint(episodeswatched):
    try:
        episodeswatched = int(episodeswatched)
    except:
        while type(episodeswatched) == str:
            try:
                episodeswatched = input("Please input a number: ")
                episodeswatched = int(episodeswatched)
            except:
                pass
    return episodeswatched

def changewatchedepisodes():
    global animelist
    chosenanimeindex = whichanime(input("Which anime are you looking for?: "), animelist)
    anime = listofanimes[animelist[chosenanimeindex]["Index"]]
    if anime["Episodes"] == "Unknown":
        anime["Episodes"] = 999
    
    print(f"Episode count: {anime['Episodes']}")
    episodeswatched = input("At what episode are you at?: ")
    episodeswatched = makeint(episodeswatched)
    while episodeswatched > int(anime["Episodes"]):
        episodeswatched = makeint(input("This episode does not exist. Try again: "))
    animelist[chosenanimeindex]["Watched Episodes"] = episodeswatched
    newsave(directory + "JSON\\lists.json", animelist)

def totalwatchtime():
    Actualduration = 0
    for i in animelist:
        try:
            index = i["Index"]
            animeinfo = listofanimes[index]
            if not animeinfo["Episodes"] == "Unknown" and not animeinfo["Duration"] == "Unknown":
                Actualduration += (int(animeinfo["ActualDuration"]) * int(i["Watched Episodes"]))
            elif animeinfo["Duration"] != "Unknown" and animeinfo["Unknown"]:
                Actualduration += (int(animeinfo["ActualDuration"]) * int(i["Watched Episodes"]))
            Actualduration += int(animeinfo["Episodes"]) * int(animeinfo["ActualDuration"]) * int(animelist["Watched"])
        except:
            pass
    return Actualduration

def timebeenwatching(time, sec):
    timer = time // sec
    return timer, (time - (timer * sec))

def printtimewatched(list1, list2 = ["Years", "Months", "Days", "Hours", "Minutes", "Seconds"]):
    list3 = []
    for i in range(0, len(list1)):
        if list1[i] > 0:
            list3.append((list1[i], list2[i]))
    sentence = ""
    for i in range(0, len(list3)):
        sentence += f"{list3[i][0]} {list3[i][1]}, "
    print("Time spent watching anime: " + sentence[0:-2])

def viewstats():
    global animelist
    timewatched = totalwatchtime()
    years, timewatched = timebeenwatching(timewatched, 31557600)
    months, timewatched = timebeenwatching(timewatched, 2629800)
    days, timewatched = timebeenwatching(timewatched, 86400)
    hours, timewatched = timebeenwatching(timewatched, 3600)
    minutes, timewatched = timebeenwatching(timewatched, 60)
    printtimewatched([years, months, days, hours, minutes, timewatched])

def whichfolder():
    directory2 = input("What is the directory?: ") + "\\"
    try:
        yep = [x[0] for x in walk(directory2)]
    except:
        print("This path does not exist. Returning to Main Menu.")
        return
    yep.pop(0)
    return yep, directory2

def addbyfolder():
    yep, directory2 = whichfolder()
    yep2 = []
    lenth = len(directory2)
    chosenlist = whichlist(input("In which list do you want to save the anime?: "))
    if chosenlist == None:
        return

    for i in yep:
        j = i[lenth:-1] + i[-1]
        yep2.append(j.replace("\\", " "))
    
    skipped = []
    for j in yep2:
        anime = whichanime(j, listofanimes)
        if anime == None:
            skipped.append(j)
        else:
            newanime = {"Index": anime, "Anime": listofanimes[anime]["Anime"], "List": chosenlist, "Watched": 0, "Watched Episodes": 0, "Rating": None}
            actualaddanime(newanime, anime, chosenlist)
    
    try:
        print("These anime were skipped:")
        for l in skipped:
            print(l)
    except:
        pass

def begin():
    a = input('What do you want to do?: ')
    if a.lower() == 'add anime' or a.lower() == 'add':
        b = input('On what way do you want to add an anime? (Anime ID/Anime name): ')
        if b.lower() == 'anime id':
            add('Anime ID')
        else:
            add('Anime')
    elif a.lower() == 'stop' or a.lower() == 'end':
        return print('Joe Joe!')
    elif a.lower() == 'print' or a.lower() == 'animelist' or a.lower() == 'print animelist':
        printanimelist()
    elif a.lower() == 'delete' or a.lower() == 'del':
        delete()
    elif a.lower() == 'add list':
        addlist()
    elif a.lower() == 'load list' or a.lower() == 'load':
        loadlist()
    elif a.lower() == 'delete list':
        deletelist()
    elif a.lower() == 'random' or a.lower() == 'random anime':
        randomanime()
    elif a.lower() == 'search':
        search()
    elif a.lower() == "settings":
        setting()
    elif a.lower() == "change listname":
        changelistname()
    elif a.lower() == "change episodes":
        changewatchedepisodes()
    elif a.lower() == "stats" or a.lower() == "show stats":
        viewstats()
    elif a.lower() == "add by folder":
        addbyfolder()
    begin()

start()
begin()

# # Change Data
# for i in range(0, len(listofanimes)):
#     if listofanimes[i]["Anime"] == 'Young Alive! ~iPS細胞がひらく未来~':
#         a = listofanimes.pop(i)
#         a["Anime"] = "Young Alive!: iPS Saibou Ga Hiraku Mirai"
#         listofanimes.insert(i, a)
#         print(listofanimes[i-1]["Anime ID"], listofanimes[i]["Anime ID"], listofanimes[i+1]["Anime ID"])