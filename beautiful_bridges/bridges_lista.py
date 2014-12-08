# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup

# Extrai o nome e a coordenada da ponte no caso que a informação está contida em uma tabela.
def extractTabela(soup,resposta):

    tables = soup.find_all('table')
    for table in tables:
        headers = table.find_all('th')
        nome=-1
        location=-1
        j=0
        loc_found = False
        for header in headers:
            if header.text == "Name":
                nome=j
            if header.text =="Coordinates":
                location=j
                loc_found = True
            if header.text =="Location" and loc_found == False:
                location=j
            j+=1
        if nome != -1 and location != -1:
            lines = table.find_all('tr')
            for line in lines:
                cells = line.find_all('td')
                if cells:
                    temp =[]
                    temp.append(cells[nome].string)
                    coords = cells[location].find_all('span')
                    for coord in coords:
                        if coord.get('class') is not None and coord['class'][0] == "geo-dec":
                                temp.append(coord.text)
                    resposta.append(temp)
                    print(temp)

#Verifica se a pagina é do tipo lista ou tabela. Retorna true se for tabela
def verificaTabela(soup):
    tables = soup.find_all('table')
    for table in tables:
        headers = table.find_all('th')
        nome=0
        location=0
        for header in headers:
            if header.text == "Name":
                nome=1
            if header.text =="Coordinates" or header.text =="Location":
                location=1
        if nome == 1 and location == 1:
            return True
    return False

# Encontra as listas na URL que não fazem parte do LI
def findLists(url,resposta,visited):
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read())

    links = soup.find_all('a')
    for link in links:
        if link.get('href') is not None and "List of " in link.text and link.parent.name != "li":
            recuperaPontes('https://en.wikipedia.org'+link['href'],resposta,visited)

# Verifica se o tipo da pagina é tabela ou não, se não for tabela ela adquire a informação dos LI. Caso no LI seja uma Lista de Bridges ele chama recursivamente a função
def findElements(url,resposta,visited):
    visited.append(url)

    try:
        response = urllib.request.urlopen(url)
    except:
        print("pagina nao encontrada")
    else:
        soup = BeautifulSoup(response.read())

        findLists(url,resposta,visited)

        if verificaTabela(soup)==True:
            extractTabela(soup,resposta)
        else:
            linhas = soup.find_all('li')
            for linha in linhas:
                links = linha.find_all('a')
                if links and links[0].get('href') is not None and links[0].get('title') is not None and links[0].get('href')[0:6]=="/wiki/":
                    a=links[0]
                    if "List of bridges" in a['title']:
                        recuperaPontes('https://en.wikipedia.org'+a['href'],resposta,visited)
                    else:
                        temp=[]
                        temp.append(a['title'])
                        temp.append(getCoordinates('https://en.wikipedia.org'+a['href']))
                        resposta.append(temp)
                        print(temp)

# Extrai as coordenadas de uma pagina, caso não encontre retorna 'sem informacao'
def getCoordinates(url):
    try:
        response = request.get(url)
    except:
        return "url nao encontrada"
    else:
        soup = BeautifulSoup(response.read())

        coords = soup.find_all('span')
        for coord in coords:
            if coord.get('class') is not None and coord['class'][0] == "geo-dec":
                return coord.text
        return "sem informacao"

# INCOMPLETO. NOT IN USE. Encontra a tag h2 see also
def encontraSeeAlso(soup):
    tags_h2 = soup.find_all('h2')
    for tag_h2 in tags_h2:
        texts = tag_h2.find_all('span')
        for text in texts:
            if "See also" in text:
                return tag_h2

# INCOMPLETO, NOT IN USE. Limpa o soup a partir da tag h2 see also.
def limpaSoup(soup):
    if encontraSeeAlso(soup) is not None:
        soup.find_all_next()

    return soup

#funcao principal
def recuperaPontes(url,resposta,visited):
    if url in visited:
        pass
        print("JA VISITADO!!!!!!!!!!!!!!!")
    else:
        visited.append(url)
        print(url)
        findElements(url,resposta,visited)

correct=[]
visited=[]
recuperaPontes('https://en.wikipedia.org/wiki/List_of_bridges',correct,visited)
print(correct)
print(visited)