for i in range(11501, 20000):
    print(str(i))
    if i % 100 == 0:
        open_file = open(directory + 'Tests/' + file_name, "wb")
        pickle.dump(listofanimes, open_file)
        open_file.close()
        print(len(listofanimes))
    time.sleep(2.5)
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

        dictionary = {"Anime" : f"{page_soup.h1.text}", "Anime ID" : f"{i}", "Type" : f"{f}",
                     "Episodes" : f"{b.replace('Episodes:', '').strip()}", "Aired" : f"{c}", "Genres" : e,
                     "Duration" : f"{g.replace('Duration:', '').strip()}"}

        listofanimes.append(dictionary)
    except:
        pass

open_file = open(directory + 'Tests/' + file_name, "wb")
pickle.dump(listofanimes, open_file)
open_file.close()