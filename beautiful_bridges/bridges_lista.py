# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup

response = urllib.request.urlopen('https://en.wikipedia.org/wiki/List_of_bridges')

soup = BeautifulSoup(response.read())

resposta = []

textos = soup.find_all('h2')
# for texto in textos:
#     if "See also" in texto.text:
#         while texto.next_siblings.next:




links = soup.find_all('a')
for link in links:
    if link.get('href') is not None and "List of " in link.text and link.parent.name != "li":
        print(link.text)
        print(link['href'])


print(resposta)