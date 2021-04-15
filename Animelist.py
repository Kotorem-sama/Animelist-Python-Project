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
from os import listdir, remove, rename, mkdir
from os.path import isfile, join, dirname, realpath

directory = dirname(realpath(__file__)) + '\\'
lists = []
settings = None
list_name = None
animelist = []
listofanimes = []
emptyanimelist = [{"List": "Watching"}, {"List": "Completed"}, {"List": "On Hold"}, {"List": "Dropped"}, {"List": "Plan to Watch"}]
emptysettings = {"lastanimelist": "Watching", "standardlist": False, "standardlistname": "Watching", "sorting": "Anime"}

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
    try:
        data = newload(folderdirectory + "\\" + filename)
    except:
        try:
            mkdir(folderdirectory)
            newsave(folderdirectory + "\\" + filename, emptystate)
            data = emptystate
        except:
            newsave(folderdirectory + "\\" + filename, emptystate)
            data = emptystate
    return data

# Loads the first bits.
def start():
    global lists, settings, list_name, listofanimes, animelist
    settings = filedoesnotexistfix("settings.json", directory + "JSON", emptysettings)
    listofanimes = newload(directory + "JSON\\listofanimes.json")
    animelist = filedoesnotexistfix("lists.json", directory + "JSON", emptyanimelist)
    lists = []
    for m in animelist:
        if m["List"] not in lists:
            lists.append(m["List"])
    if settings["standardlist"] == True:
        file_name = settings["standardlistname"]
    else:
        file_name = settings["lastanimelist"]
    
    print(f"You are currently viewing '{file_name}'")

header = {
    'host': 'crunchyroll.com',
    'referer': 'https://www.google.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
}

# # Saves the animelist to json.
# def save(filename):
#     with open(directory + "JSON\\Lists\\" + filename + ".json", "w") as f:
#         json.dump(json.dumps(animelist), f)

# Returns a list of anime names that now have the same length as the input.
def lengthmaker(checklist, length):
    checklist2 = []
    for i in checklist:
        newword = i.ljust(length, ' ')
        newword = newword[0:length]
        checklist2.append(newword)
    return checklist2

# Returns a list for the similarity check with anime names.
def checklistmaker(i):
    checklist = [listofanimes[i]["Anime"]]
    if listofanimes[i]["English"] != '':
        checklist.append(listofanimes[i]["English"])
    if listofanimes[i]["Synonyms"] != []:
        for yikerss in listofanimes[i]["Synonyms"]:
            checklist.append(yikerss)
    return checklist

# Returns the anime that resembles the input the most.
def maximumsimilarity(a):
    maximum = 50
    maximumanimelist = []
    a = a.lower()
    for i in range(0, len(listofanimes)):
        checklist = lengthmaker(checklistmaker(i), len(a))
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
    try:
        with uReq(URL) as uClient:
            page_html = uClient.read()
        page_soup = soup(page_html, "html.parser")
    except:
        page_soup = soup()
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
        Episodes = myanimelistpage.find('span', text="Episodes:").find_previous('div').text
        Episodes = Episodes.replace('Episodes:', '').strip()
        listofanimes[b]['Episodes'] = Episodes
    if listofanimes[b]['Aired'] == "Not available" or listofanimes[b]['Aired'][-1] == "?":
        try:
            Aired = myanimelistpage.find('span', text="Premiered:").find_next('a').text
            Aired = Aired.replace('Premiered:', '').strip()
        except:
            Aired = myanimelistpage.find('span', text="Aired:").find_previous('div').text
            Aired = Aired.replace('Aired:', '').strip()
        listofanimes[b]['Aired'] = Aired
    if listofanimes[b]['Duration'] == "Unknown":
        Duration = myanimelistpage.find('span', text="Duration:").find_previous('div').text
        Duration = Duration.replace('Duration:', '').strip()
        listofanimes[b]['Duration'] = Duration

def whichanime():
    a = input("Which anime are you looking for?: ")
    if a.lower() == 'stop' or a.lower() == 'end' or a.lower() == 'cancel':
        return None
    outcome = maximumsimilarity(a)
    if len(outcome) == 1:
        b = int(outcome[0])
    elif len(outcome) == 0:
        print("You really need to learn how to type")
        return None
    else:
        for i in range(0, len(outcome)):
            print(f"{i + 1}. {listofanimes[outcome[i]]['Anime']} (English: {listofanimes[outcome[i]]['English']}) (Type: {listofanimes[outcome[i]]['Type']})")
        d = input('Which anime do you wish to know more about? (number/stop): ')
        try:
            d = int(d)
            b = int(outcome[d - 1])
        except:
            print('Process Cancelled')
            return None
    return b

def search():
    b = whichanime()
    if b == None:
        pass
    else:
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
                elif key == "Anime ID":
                    value2 = 'https://myanimelist.net/anime/' + value
                    myanimelistpage = page_soupgetter(value2)
                    Score = myanimelistpage.find('span', text="Score:").find_next('span').text
                    print("Score:              " + Score)
                else:
                    value2 = value
                spaces = (19 - len(key)) * " "
                print(key + ':' + spaces + value2)
        changes(b, myanimelistpage)
        print(f"Where to watch:     {wheretowatch(checklistmaker(b), None)}")

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
    if a.lower() == 'stop' or a.lower() == 'end' or a.lower() == 'cancel':
        pass
    elif a in lists:
        b = input("Are you sure you want to delete '" + a + "'? (yes/no): ")
        if b.lower() == 'yes':
            lists.remove(a)
            actualdeletelist(a)
            print(lists)
            c = input('Which list do you want to load?: ')
            while c not in lists:
                c = input('This list does not exist. Try again: ')
            load(c)
            print("Loaded list '" + c + "'")
    else:
        print('This list does not exist.')
        deletelist()

def add(wayf):
    global animelist
    newanime = {"Index": "", "Anime": "", "List": list_name, "Watched": 0, "Watched Episodes": 0, "Rating": None}
    if wayf == 'Anime ID':
        c = ''
        a = input("What is the Anime ID?: ")
        if a.lower() == 'stop' or a.lower() == 'end' or a.lower() == 'cancel':
            pass
        else:
            for i in range(0, len(listofanimes)):
                if str(listofanimes[i]["Anime ID"]) == str(a):
                    c = i
            if c == '':
                print('This Anime ID does not exist.')
                add(wayf)
            else:
                newanime["Index"] = c
                newanime["Anime"] = listofanimes[c]["Anime"]
                inlist = False
                for l in animelist:
                    if l["Index"] == c:
                        inlist = True
                if inlist:
                    print("Anime already in animelist")
                else:
                    b = input("Are you sure you want to add '" + listofanimes[c]["Anime"] + "'?: ")
                    if b.lower() == 'yes' or b == '':
                        animelist.append(newanime)
                        newsave(directory + "JSON\\lists.json", animelist)
                add(wayf)
    elif wayf == 'Anime':
        a = whichanime()
        if a == None:
            pass
        else:
            newanime["Index"] = a
            newanime["Anime"] = listofanimes[a]["Anime"]
            if newanime in animelist:
                print("Anime already in animelist")
            else:
                animelist.append(newanime)
                newsave(directory + "JSON\\lists.json", animelist)
            add(wayf)

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
            if i["Anime"] == a:
                b = input("Are you sure you want to delete '" + i["Anime"] + "'?: ")
                if b.lower() == 'yes' or b == '':
                    animelist.remove(i)
                    newsave(directory + "JSON\\lists.json", animelist)
                    break
        if b != '':
            print('This anime does not exist in this list.')
        delete()

def whichlist():
    print(lists)
    b = input('Which list are you looking for?: ')
    if b.lower() != 'stop' or b.lower() != 'end' or b.lower() != 'cancel':
        while b not in lists:
            b = input('This list does not exist. Try again: ')
    return b

def loadlist():
    b = whichlist()
    load(b)
    print(f"You are currently viewing '{list_name}'")

def sort2():
    global animelist
    sortmode = settings["sorting"]
    for i in animelist:
        if "Anime" in i:
            checkforsortpossibility = i
            break
    if sortmode not in checkforsortpossibility:
        for j in animelist:
            j[sortmode] = listofanimes[j["Index"]][sortmode]
    animelist = sorted(animelist, key = lambda i: i[sortmode])
    newsave(directory + "JSON\\lists.json", animelist)
    print('Sorting Complete!')

def printanimelist():
    a = 1
    global animelist
    for i in animelist:
        print(str(a) + '. ' + i["Anime"])
        a += 1

def randomanime():
    global animelist
    print(choice(animelist)["Anime"])

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
    chosenlist = whichlist()
    settings[a] = chosenlist

def whichsetting():
    a = input("Which setting do you want to change?: ")
    if a.lower() == 'stop' or a.lower() == 'end':
        pass
    else:
        while a not in settings:
            a = input("This setting does not exist. Try again: ")
        if type(settings[a]) == bool:
            trueorfalsesetting(a)
        elif a == "lastanimelist" or a == "standardlistname" == a:
            listsetting(a)

def changename(listname, newlistname):
    global lists
    lists.remove(listname)
    lists.append(newlistname)
    rename(directory + '\\JSON\\Lists\\' + listname + ".json", directory + '\\JSON\\Lists\\' + newlistname + ".json")
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
    elif a.lower() == 'sort' or a.lower() == 'sort list':
        sort2()
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
        name = whichlist()
        newname = input("What will the new name of the list be?: ")
        changename(name, newname)
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