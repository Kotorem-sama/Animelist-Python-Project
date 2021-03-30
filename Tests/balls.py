from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio() * 100

a = 'https://www.masterani.one/watch/shirobako-specials-2015.html'
b = 'https://www.masterani.one/watch/shirobako-specials-2015.html'

print(similarity(a.lower(), b.lower()))