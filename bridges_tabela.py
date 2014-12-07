import urllib.request

from bs4 import BeautifulSoup

response = urllib.request.urlopen('https://en.wikipedia.org/wiki/'+'List_of_bridges_on_the_National_Register_of_Historic_Places_in_Alabama')

soup = BeautifulSoup(response.read())

resposta = []

tables = soup.find_all('table')
for table in tables:
    headers = table.find_all('th')
    nome=-1
    location=-1
    j=0
    for header in headers:
        if header.text == "Name":
            nome=j
            print(nome)
        if header.text =="Location":
            location=j
            print(location)
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


print(resposta)