import pickle
import os
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

directory = os.path.dirname(os.path.realpath(__file__)) + '\\'
file_name = "Seasonal.pkl"
animelist = lists = listofanimes = []
deleted = False
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
def checklistmaker(i):
    checklist = [listofanimes[i]["Anime"]]
    if listofanimes[i]["English"] != '':
        checklist.append(listofanimes[i]["English"])
    try:
        for yikerss in listofanimes[i]["Synonyms"]:
            checklist.append(yikerss)
    except:
        pass
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
        uClient = uReq(URL)
        page_html = uClient.read()
        uClient.close()
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
    print(attempt)
    r = req.get(attempt, timeout=20, headers=header)
    if r.status_code == 200:
        return r.url

# Returns the first link that exists or returns the text 'Not Found...'. In that case i will try to find an accessible
# website where you can watch it.
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

def whichanime():
    a = input("Which anime do you wish to know more about?: ")
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

def search():
    b = whichanime()
    print(b)
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
    print(f"Where to watch:     {wheretowatch(checklistmaker(b))}")

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio() * 100

def load(file_name2):
    global directory, animelist, deleted
    if not deleted:
        open_file = open(directory + 'Lists/' + file_name, "wb")
        pickle.dump(animelist, open_file)
        open_file.close()

    open_file = open(directory + 'Lists/' + file_name2, "rb")
    animelist = pickle.load(open_file)
    open_file.close()
    globalfile_name(file_name2)
    deleted = False

def globalfile_name(a):
    global file_name
    file_name = a

def addlist():
    global lists, directory
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
    
    if listname != '':
        lists.append(listname)
        open_file = open(directory + "Lists.pkl", "wb")
        pickle.dump(lists, open_file)
        open_file.close()

        newanimelist = []
        open_file = open(directory + 'Lists/' + listname + '.pkl', "wb")
        pickle.dump(newanimelist, open_file)
        open_file.close()

        c = input('Do you want to load ' + listname + '?: ')
        if c.lower() == 'yes':
            load(listname + '.pkl')

def deletelist():
    global lists, deleted
    print(lists)
    a = input('Which list do you want to delete?: ')
    if a.lower() == 'stop' or a.lower() == 'end' or a.lower() == 'cancel':
        pass
    elif a in lists:
        b = input("Are you sure you want to delete '" + a + "'? (yes/no): ")
        if b.lower() == 'yes':
            lists.remove(a)
            open_file = open(directory + "Lists.pkl", "wb")
            pickle.dump(lists, open_file)
            open_file.close()
            path = directory + "Lists/" + a + ".pkl"
            os.remove(path)
            print(lists)
            c = input('Which list do you want to load?: ')
            while c not in lists:
                c = input('This list does not exist. Try again: ')
            deleted = True
            load(c + '.pkl')
            print("Loaded list '" + c + "'")
    else:
        print('This list does not exist.')
        deletelist()

def add(wayf):
    global animelist
    a = input('Anime to add: ')
    if a.lower() == 'stop' or a.lower() == 'end' or a.lower() == 'cancel':
        pass
    elif a in animelist:
        print('This anime is already in the list.')
        add(wayf)
    else:
        if wayf == 'Anime ID':
            c = 'Not in the lixst'
            for i in range(0, len(listofanimes)):
                if str(listofanimes[i]["Anime ID"]) == str(a):
                    c = listofanimes[i]["Anime"]
            if c == 'Not in the list':
                print('This Anime ID does not exist.')
                add(wayf)
            else:
                b = input("Are you sure you want to add ' " + c + " '?: ")
                if b.lower() == 'yes' or b == '':
                    animelist.append(c)
                add(wayf)
        elif wayf == 'Anime':
            maximumanimelist = maximumsimilarity(a)
            if len(maximumanimelist) != 1:
                for i in range(0, len(maximumanimelist)):
                    print(f"{i + 1}. {listofanimes[maximumanimelist[i]]['Anime']} (English: {listofanimes[maximumanimelist[i]]['English']}) (Type: {listofanimes[maximumanimelist[i]]['Type']})")
                d = input('Which anime do you wish to add? (number/stop): ')
                try:
                    d = int(d)
                    chosenanime = int(maximumanimelist[d - 1])
                    chosenanime2 = listofanimes[chosenanime]["Anime"]
                    e = input("Are you sure you want to add ' " + chosenanime2 + " '? (yes/no): ")
                    if e.lower() == 'yes':
                        animelist.append(chosenanime2)
                    else:
                        print('Process Cancelled') 
                except:
                    print('Process Cancelled')
                add(wayf)
            elif len(maximumanimelist) == 0:
                print("That's not funny. Get lost")
                return
            else:
                maximumanime = maximumanimelist[0]
                if maximumanime in animelist:
                    print("No new anime found")
                else:
                    d = input(f"Do you wish to add '{listofanimes[maximumanime]['Anime']} (English: {listofanimes[maximumanime]['English']})'? (yes/no): ")
                    if d == 'yes':
                        animelist.append(listofanimes[maximumanime]["Anime"])
                add(wayf)

def delete():
    global animelist
    a = input('Which anime do you want to remove from the list: ')
    if a.lower() == 'stop' or a.lower() == 'end' or a.lower() == 'cancel':
        pass
    elif a.lower() == 'help' or a.lower() == 'print':
        printanimelist()
        delete()
    elif a in animelist:
        b = input("Are you sure you want to delete '" + a + "'?: ")
        if b.lower() == 'yes' or b == '':
            c = animelist.index(a)
            animelist.pop(c)
        delete()
    else:
        print('This anime does not exist in this list.')
        delete()
        

def sort2():
    global animelist
    animelist.sort()
    print('Sorting Complete!')

def printanimelist():
    a = 1
    global animelist
    for i in animelist:
        print(str(a) + '. ' + i)
        a += 1

def randomanime():
    global animelist
    print(choice(animelist))

def begin2():
    global animelist, file_name, lists, listofanimes
    open_file = open(directory + 'Lists\\' + file_name, "rb")
    animelist = pickle.load(open_file)
    open_file.close()

    open_file = open(directory + "Lists.pkl", "rb")
    lists = pickle.load(open_file)
    open_file.close()
    
    open_file = open(directory + 'Tests/' + 'Listofanimes.pkl', "rb")
    listofanimes = pickle.load(open_file)
    open_file.close()
    listofanimes = listofanimes

    print("Loaded list 'Seasonal'")
    begin()

def begin():
    global animelist, file_name
    load(file_name)
    a = input('What do you want to do?: ')
    if a.lower() == 'add anime' or a.lower() == 'add':
        b = input('On what way do you want to add an anime? (Anime ID/Anime name): ')
        if b.lower() == 'anime id':
            add('Anime ID')
        else:
            add('Anime')
    elif a.lower() == 'stop' or a.lower() == 'end':
        open_file = open(directory + 'Lists/' + file_name, "wb")
        pickle.dump(animelist, open_file)
        open_file.close()
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
        print(lists)
        b = input('Which list do you want to load?: ')
        if b.lower() != 'stop' or b.lower() != 'end' or b.lower() != 'cancel':
            while b not in lists:
                b = input('This list does not exist. Try again: ')
            load(b + '.pkl')
            print("Loaded list '" + b + "'")
    elif a.lower() == 'delete list':
        deletelist()
    elif a.lower() == 'random' or a.lower() == 'random anime':
        randomanime()
    elif a.lower() == 'search':
        search()
    begin()

# begin2()

open_file = open(directory + 'Tests/' + 'Listofanimes.pkl', "rb")
listofanimes = pickle.load(open_file)
open_file.close()

for i in listofanimes:
    for j in range(0, len(i["Anime"])):
        try:
            if i["Anime"][j-1] != " " and i["Anime"][j] == "x" and i["Anime"][j+1] != " ":
                print(i["Anime"])
        except:
            pass

# b = "！"
# a = []

# for yikers in b:
#     a.append(yikers)

# listofanimewithrandomcharacters = []
# listending = []

# # hebben char in naam
# for i in listofanimes:
#     for j in i["Anime"]:
#         if j in a:
#             listofanimewithrandomcharacters.append(i["Anime"])

# # Eindigd op char
# for i in listofanimes:
#     if i["Anime"][-1] in a:
#         listending.append(i["Anime"])

# print('ending:')
# for i in listending:
#     print(i)

# print('\nwith:')
# for i in listofanimewithrandomcharacters:
#     print(i)

# # Search for data
# for i in listofanimes:
#     if i["Anime"] == "マンキーのアニメレビュー":
#         print(i)

# # Change Data
# for i in range(0, len(listofanimes)):
#     if listofanimes[i]["Anime"] == 'Young Alive! ~iPS細胞がひらく未来~':
#         a = listofanimes.pop(i)
#         a["Anime"] = "Young Alive!: iPS Saibou Ga Hiraku Mirai"
#         listofanimes.insert(i, a)
#         print(listofanimes[i-1]["Anime ID"], listofanimes[i]["Anime ID"], listofanimes[i+1]["Anime ID"])


# for i in range(1, len(listofanimes)):
#     if int(listofanimes[i]["Anime ID"]) < int(listofanimes[i-1]["Anime ID"]):
#         g = i
#         while int(listofanimes[i]["Anime ID"]) < int(listofanimes[g-1]["Anime ID"]):
#             g = g - 1
#         listofanimes.insert(g, listofanimes.pop(i))

# open_file = open(directory + 'Tests/' + 'Listofanimes.pkl', "wb")
# pickle.dump(listofanimes, open_file)
# open_file.close()

# # Searches for the biggest Anime ID gap
# index1 = 0
# index2 = 1
# maximum = maximumindex1 = maximumindex2 = 0
# for i in range (0, len(listofanimes)):
#     try:
#         if (int(listofanimes[index2]["Anime ID"]) - int(listofanimes[index1]["Anime ID"])) > maximum:
#             maximum = int(listofanimes[index2]["Anime ID"]) - int(listofanimes[index1]["Anime ID"])
#             maximumindex1 = index1
#             maximumindex2 = index2
#     except:
#         pass
#     index1 += 1
#     index2 += 1
# print(maximum, listofanimes[maximumindex1]["Anime ID"], listofanimes[maximumindex2]["Anime ID"])