from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pickle
import time
from playsound import playsound
import os

directory = os.path.dirname(os.path.realpath(__file__)) + '\\'
file_name = "Listofanimes.pkl"
open_file = open(directory  + 'Listofanimes.pkl', "rb")
listofanimes = pickle.load(open_file)
open_file.close()

def ActualDurationCalc(ActualDuration):
    ActualDuration2 = ActualDuration3 = ActualDuration4 = 0
    for k in range(0, len(ActualDuration)):
        if ActualDuration[k] == 'h':
            try:
                poging = int(ActualDuration[k-3])
            except:
                poging = ActualDuration[k-3]
            if type(poging) == int:
                ActualDuration2 = (int(ActualDuration[k-2]) + (10 * poging)) * 60 * 60
            else:
                ActualDuration2 = int(ActualDuration[k-2]) * 60 * 60
        elif ActualDuration[k] == 'm':
            try:
                poging = int(ActualDuration[k-3])
            except:
                poging = ActualDuration[k-3]
            if type(poging) == int:
                ActualDuration3 = (int(ActualDuration[k-2]) + (10 * poging)) * 60
            else:
                ActualDuration3 = int(ActualDuration[k-2]) * 60
        elif ActualDuration[k] == 's':
            try:
                poging = int(ActualDuration[k-3])
            except:
                poging = ActualDuration[k-3]
            if type(poging) == int:
                ActualDuration4 = int(ActualDuration[k-2]) + (10 * poging)
            else:
                ActualDuration4 = int(ActualDuration[k-2])
    return ActualDuration2 + ActualDuration3 + ActualDuration4

for i in range(48613, 49000):
    print(str(i))
    if i % 100 == 0:
        open_file = open(directory + file_name, "wb")
        pickle.dump(listofanimes, open_file)
        open_file.close()
        print(len(listofanimes))
    time.sleep(2.6)
    try:
        uClient = uReq('https://myanimelist.net/anime/' + str(i))
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")

        b = page_soup.find('span', text="Episodes:").find_previous('div').text
        f = page_soup.find('span', text="Type:").find_next('a').text
        try:
            c = page_soup.find('span', text="Premiered:").find_next('a').text
        except:
            c = page_soup.find('span', text="Aired:").find_previous('div').text
            c = c.replace('Aired:', '').strip()
        d = page_soup.find('span', text="Genres:").find_previous('div')
        d = d.findAll('span', {"itemprop":"genre"})
        e = [d[0].text]
        for j in range(1, len(d)):
            e.append(d[j].text)
        g = page_soup.find('span', text="Duration:").find_previous('div').text
        try:
            h = page_soup.find('span', text="English:").find_previous('div').text
            h = h.replace('English:', '').strip()
        except:
            h = ''
        try:
            k = page_soup.find('span', text="Synonyms:").find_previous('div').text
            k = k.replace('Synonyms:', '').strip() + ','
            newindex = 0
            n = ''
            o = []
            for l in range(0, len(k)):
                if k[l] == ',':
                    for m in range(newindex, l):
                        n = n + str(k[m])
                    newindex = l + 2
                    o.append(n)
                    n = ''
        except:
            o = ''
        try:
            p = page_soup.find('span', text="Rating:").find_previous('div').text
            p = p.replace('Rating:', '').strip()
        except:
            p = ''
        if not (g == "Unknown") and not (b == "Unknown"):
            ActualDuration2 = ActualDurationCalc(g)
        else:
            ActualDuration2 = '?'

        dictionary = {"Anime" : f"{page_soup.h1.text}", "English" : f"{h}", "Synonyms" : f"{o}", "Anime ID" : f"{i}",
                     "Type" : f"{f}", "Episodes" : f"{b.replace('Episodes:', '').strip()}", "Aired" : f"{c}", "Genres" : e,
                     "Duration" : f"{g.replace('Duration:', '').strip()}", "Rating" : f"{p}", "ActualDuration" : f"{ActualDuration2}"}
        listofanimes.append(dictionary)
    except:
        pass
open_file = open(directory + file_name, "wb")
pickle.dump(listofanimes, open_file)
open_file.close()

open_file = open(directory + "backup.pkl", "wb")
pickle.dump(listofanimes, open_file)
open_file.close()
playsound(r'C:\Users\Kniplip\Downloads\a.wav')