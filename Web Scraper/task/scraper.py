import requests
import re
import os
from bs4 import BeautifulSoup
from string import punctuation


def pristupi_stranici(url):
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r.status_code != 200:
        print(f'The URL returned {r.status_code}!')
        return
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def sredi_naslov(naslov):
    n = naslov.replace(' ', '_')
    for znak in punctuation:
        if znak == '_':
            continue
        n = n.replace(znak, ' ')
    n = n.replace(' ', '')
    return n


def sacuvaj_u_fajl(naslov, sadrzaj, direktorija):
    fajl_naziv = f'{direktorija}/{naslov}.txt'
    os.makedirs(os.path.dirname(fajl_naziv), exist_ok=True)
    fajl = open(fajl_naziv, 'w', encoding='UTF-8')
    fajl.write(sadrzaj)
    artikli_lista.append(f'{naslov}.txt')
    fajl.close()


def sredi_tip_stranice(tip_s):
    return tip_s.replace(' ', '')


def glavna():
    url = 'https://www.nature.com/nature/articles'
    soup = pristupi_stranici(url)
    stranice = int(input())
    tip_s = input()
    tip_stranice = sredi_tip_stranice(tip_s.strip())
    for i in range(1, stranice + 1):
        flag = True
        direktorija = f'Page_{i}'
        if i != 1:
            url = 'https://www.nature.com/nature/articles'
            soup = pristupi_stranici(url)
            link = 'https://www.nature.com'
            stranice_link = soup.find_all('li', class_='c-pagination__item')
            test = soup.find('div', class_="u-container u-mb-48")
            for s in stranice_link:
                if s.get('data-test') == f'page-{i}':
                    link += s.a.get('href')
            soup = pristupi_stranici(link)
        artikli = soup.find_all('article')
        for artikal in artikli:
            tip = artikal.find('span', class_="c-meta__item")
            alo = re.sub('[^a-zA-Z]+', '', tip.text)
            if alo == tip_stranice:
                url = 'https://www.nature.com'
                url += artikal.a.get('href')
                soup = pristupi_stranici(url)
                naslov = soup.find('h1')
                naslov_sredjen = sredi_naslov(naslov.text.strip())
                sadrzaj = soup.find('div', class_="c-article-body u-clearfix")
                sadrzaj2 = soup.find('div', class_="article-item__body")
                sadrzaj3 = soup.find('div', class_="c-article-body")
                lista = [sadrzaj, sadrzaj2, sadrzaj3]
                for s in lista:
                    if s is not None:
                        sacuvaj_u_fajl(naslov_sredjen, s.text.strip(), direktorija)
                        flag = False
                        break
        if flag:
            putanja = os.getcwd().replace('\\', '/')
            os.makedirs(f'{putanja}\{direktorija}', exist_ok=True)
    print(f'Saved articles: {artikli_lista}')


artikli_lista = []
glavna()
