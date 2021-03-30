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
useragents = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Vivaldi/3.7",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Vivaldi/3.7"]
header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en;q=0.9,nl;q=0.8,ja;q=0.7',
    'connection': 'keep-alive',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-fetch-dest': 'document',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'host': 'crunchyroll.com',
    'referer': 'https://www.google.com/',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
}

# Returns a list of anime names that now have the same length as the input.
def lengthmaker(checklist, length):
    checklist2 = []
    for i in checklist:
        newword = ''
        if not len(i) < length:
            for j in range(0, length):
                newword += i[j]
            checklist2.append(newword)
    return checklist2

# Returns a list for the similarity check with anime names.
def checklistmaker(i, length):
    checklist = [listofanimes[i]["Anime"]]
    if listofanimes[i]["English"] != '':
        checklist.append(listofanimes[i]["English"])
    if listofanimes[i]["Synonyms"] != []:
        for k in listofanimes[i]["Synonyms"]:
            checklist.append(k)
    return lengthmaker(checklist, length)

# Returns the anime that resembles the input the most.
def maximumsimilarity(a):
    maximum = 50
    maximumanimelist = []
    a = a.lower()
    for i in range(0, len(listofanimes)):
        checklist = checklistmaker(i, len(a))
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

def namelistmaker(namelist):
    namelist2 = []
    for a in namelist:
        a = a.replace('(TV)', '')
        newthing = (a.replace(':', '').replace('.', '').replace('/', '').replace(' ', '-').replace('%', '').replace('(', '').replace(')', '').replace('!', '').replace('?', '').replace('<', '').replace('>', '').replace("'", "").replace("~", '').replace('☆', '').replace('&', '').replace('#', '').replace('"', '').replace(';', ''))
        liss = list(newthing)
        newthing = ''
        for c in range(0, len(liss)):
            try:
                if liss[c] == '-' and liss[c+1] == '-':
                    liss.pop(c)
            except:
                pass
        for character in liss:
            newthing += character
        if newthing.lower() not in namelist2:
            namelist2.append(newthing.lower())
    return namelist2

def Linkchecker(Cleanlink, name, header=header):
    attempt = Cleanlink + name
    r = req.get(attempt, timeout=20, headers=header)
    if r.status_code == 200:
        return r.url

def wheretowatch(namelist, year):
    namelist = namelistmaker(namelist)
    for i in namelist:

        # Kickassanime Checker
        yikers = Linkchecker("http://www2.kickassanime.rs/anime/", i, None)
        if yikers != "https://www2.kickassanime.rs/" and yikers != "https://www2.kickassanime.rs/anime/" and yikers != None:
            return yikers
        
        # Gogoanime Checker
        yikers = Linkchecker("https://gogoanime.ai/category/", i, None)
        if yikers != None:
            return yikers
        
        # Kissanime Checker
        yikers = Linkchecker("https://kissanime.ru.com/series/", i, None)
        if yikers != None:
            return yikers

        # Animeshow Checker
        yikers = Linkchecker("https://www1.animeshow.tv/", i, None)
        if yikers != None and yikers != 'https://www1.animeshow.tv':
            return yikers

        # Animefreak Checker
        yikers = Linkchecker("https://www.animefreak.tv/watch/", i, None)
        if yikers != None:
            return yikers

        # # Masterani Checker
        # try:
        #     year2 = int(year[-4] + year[-3] + year[-2] + year[-1])
        #     yikers = Linkchecker('https://www.masterani.one/watch/', i)
        #     if yikers != None:
        #         return yikers
        # except:
        #     pass

        # # Crunchyroll Checker
        # Cleanlink = 'https://www.crunchyroll.com/en-gb/'
        # attempt = Cleanlink + i
        # print(attempt)
        # try:
        #     req = urllib.request.Request(attempt, headers=header)
        #     cj = CookieJar()
        #     opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPRedirectHandler)
        #     response = opener.open(req)
        #     response.close()
        #     print(response)
        # except urllib.request.HTTPError as inst:
        #     output = format(inst)
        #     print(output)

        # # Animetake Checker
        # yikers = Linkchecker("https://animetake.tv/anime/", i, {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'})
        # if yikers != None:
        #     return yikers

        # # Animefrenzy Checker
        # yikers = Linkchecker("https://animefrenzy.org/anime/", i, None)
        # if yikers != None:
        #     return yikers

    return 'Not Found...'

def search():
    global listofanimes
    a = input("Which anime do you wish to know more about?: ")
    outcome = maximumsimilarity(a)
    if len(outcome) == 1:
        b = int(outcome[0])
    elif len(outcome) == 0:
        print("That's not funny. Get lost")
        return
    else:
        for i in range(0, len(outcome)):
            print(f"{i + 1}. {listofanimes[outcome[i]]['Anime']} (English: {listofanimes[outcome[i]]['English']}) (Type: {listofanimes[outcome[i]]['Type']})")
        d = input('Which anime do you wish to know more about? (number/stop): ')
        try:
            d = int(d)
            b = int(outcome[d - 1])
        except:
            print('Process Cancelled')
            return
    print(f"Title:          {listofanimes[b]['Anime']}")
    if listofanimes[b]['English'] != '':
        print(f"English Title:  {listofanimes[b]['English']}")
    try:
        synonymlist = listofanimes[b]['Synonyms']
        synonyms = synonymlist.pop(0)
        try:
            for j in synonymlist:
                synonyms += ', ' + j
        except:
            pass
        print(f"Synonyms:       {synonyms}")
    except:
        pass
    URL = 'https://myanimelist.net/anime/' + (listofanimes[b]['Anime ID'])
    myanimelistpage = page_soupgetter(URL)
    Change = False
    if listofanimes[b]['Episodes'] == "Unknown":
        Episodes = myanimelistpage.find('span', text="Episodes:").find_previous('div').text
        Episodes = Episodes.replace('Episodes:', '').strip()
        Change = True
    else:
        Episodes = listofanimes[b]['Episodes']
    if listofanimes[b]['Aired'] == "Not available" or listofanimes[b]['Aired'][-1] == "?":
        try:
            Aired = myanimelistpage.find('span', text="Premiered:").find_next('a').text
            Aired = Aired.replace('Premiered:', '').strip()
        except:
            Aired = myanimelistpage.find('span', text="Aired:").find_previous('div').text
            Aired = Aired.replace('Aired:', '').strip()
        Change = True
    else:
        Aired = listofanimes[b]['Aired']
    if listofanimes[b]['Duration'] == "Unknown":
        Duration = myanimelistpage.find('span', text="Duration:").find_previous('div').text
        Duration = Duration.replace('Duration:', '').strip()
        Change = True
    else:
        Duration = listofanimes[b]['Duration']
    Score = myanimelistpage.find('span', text="Score:").find_next('span').text
    print(f"Score:          {Score}")
    print(f"Myanimelist:    {URL}")
    print(f"Type:           {listofanimes[b]['Type']}")
    print(f"Episodes:       {Episodes}")
    print(f"Airdate:        {Aired}")
    try:
        synonymlist = listofanimes[b]['Genres']
        synonyms = synonymlist.pop(0)
        try:
            for j in synonymlist:
                synonyms += ', ' + j
        except:
            pass
        print(f"Genres:         {synonyms}")
    except:
        pass
    print(f"Duration:       {listofanimes[b]['Duration']}")
    print(f"Rating:         {listofanimes[b]['Rating']}")
    if Change:
        dictionary = {"Anime" : f"{listofanimes[b]['Anime']}", "English" : f"{listofanimes[b]['English']}", "Synonyms" : listofanimes[b]['Synonyms'], "Anime ID" : f"{b}",
                     "Type" : f"{listofanimes[b]['Type']}", "Episodes" : f"{Episodes}", "Aired" : Aired, "Genres" : listofanimes[b]['Genres'],
                     "Duration" : f"{Duration}", "Rating" : listofanimes[b]['Rating'], "ActualDuration" : listofanimes[b]['ActualDuration']}
        listofanimes.pop(b)
        listofanimes.append(dictionary)
    namelist = [listofanimes[b]['Anime']]
    if listofanimes[b]['English'] != '':
        namelist.append(listofanimes[b]['English'])
    try:
        for i in listofanimes[b]['Synonyms']:
            namelist.append(i)
    except:
        pass
    print(f"Where to watch: {wheretowatch(namelist, Aired)}")

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

begin2()

# open_file = open(directory + 'Tests/' + 'Listofanimes.pkl', "rb")
# listofanimes = pickle.load(open_file)
# open_file.close()

# for i in range(0, len(listofanimes)):
#     if listofanimes[i]["Anime ID"] == '28121':
#         print(listofanimes[i]["Synonyms"][1])

# for i in range(1, len(listofanimes)):
#     if int(listofanimes[i]["Anime ID"]) < int(listofanimes[i-1]["Anime ID"]):
#         g = i
#         while int(listofanimes[i]["Anime ID"]) < int(listofanimes[g-1]["Anime ID"]):
#             g = g - 1
#         listofanimes.insert(g, listofanimes.pop(i))

# open_file = open(directory + 'Tests/' + 'Listofanimes.pkl', "wb")
# pickle.dump(listofanimes, open_file)
# open_file.close()

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