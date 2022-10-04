#AB #81

import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

#swbg

def swbg3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\swbg_03.csv'
        titulos = []
        titulos2 = []
        textos = []
        textos2 = []
        links = ['https://swbg-conservationfund.org/about-us/', 'https://swbg-conservationfund.org/grant-seekers/']

        page = Request('https://swbg-conservationfund.org/about-us/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('span', style = 'text-align:center').get_text()
        texto = soup.find('div', class_ = 'page-teaser rtf container').get_text()

        page2 = Request('https://swbg-conservationfund.org/grant-seekers/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request2 = urlopen(page2).read()
        soup2 = BeautifulSoup(page_request2, 'lxml')
        titulo2 = soup2.find('h2', class_ = 'page-sub-headline container text-left').get_text()
        texto2 = soup2.find('div', class_= 'page-teaser rtf container text-left').get_text()

        titulos.append(titulo)
        titulos2.append(titulo2)
        textos.append(clean(texto))
        textos2.append(clean(texto2))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos + titulos2
        df['pol_instituicao'] = ['swbg'] * len(df.index)
        df['pol_texto'] = textos + textos2
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'swbg_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em swbg3')
        
#swbg3('.')