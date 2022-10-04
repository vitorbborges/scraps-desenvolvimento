#AB #35

import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

def newtonfund3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\newtonfund_03.csv'
        titulos = []
        titulos2 = []
        titulos3 = []
        textos = []
        textos2 = []
        textos3 = []
        links = ['https://www.newton-gcrf.org/newton-fund/', 'https://www.newton-gcrf.org/transparency/', 'https://www.newton-gcrf.org/newton-fund/newton-prize/']


        page = Request('https://www.newton-gcrf.org/newton-fund/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('div', class_ = 'banner__text').get_text()
        texto = soup.find('div', class_ = 'tcti__left').get_text()

        page2 = Request('https://www.newton-gcrf.org/transparency/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request2 = urlopen(page2).read()
        soup2 = BeautifulSoup(page_request2, 'lxml')
        titulo2 = soup2.find('span', class_ = 'current').get_text()
        texto2 = soup2.find('div', class_ = 'panel-layout').get_text()

        page3 = Request('https://www.newton-gcrf.org/newton-fund/newton-prize/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request3 = urlopen(page3).read()
        soup3 = BeautifulSoup(page_request3, 'lxml')
        titulo3 = soup3.find('div', class_ = 'dl-page__heading').get_text()
        texto3 = soup3.find('p').get_text()

        titulos.append(clean(titulo))
        textos.append(clean(texto))
        titulos2.append(clean(titulo2))
        textos2.append(clean(texto2))
        titulos3.append(clean(titulo3))
        textos3.append(clean(texto3))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos + titulos2 + titulos3 
        df['pol_instituicao'] = ['newtonfund'] * len(df.index)
        df['pol_texto'] = textos + textos2 + textos3
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'newtonfund_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path+filename, index = False)
    
    except Exception as e:
        print(e)
        print('Erro em newtonfund3')
        
#newtonfund3('.')
