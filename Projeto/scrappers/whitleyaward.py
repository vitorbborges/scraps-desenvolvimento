# AB#51
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
from itertools import compress
from urllib.request import Request, urlopen
from utilidadesppf import getCodList, getNewInfo, clean

# SITE PROTEGIDO POR JAVASCRIPT

#whitleyaward2
def whitleyaward2(path, keywords = '(brazil|latin america region)'):
    try:   
        dia = datetime.today().strftime('%y%m%d')
        filename = '/whitleyaward_02.csv'
        titulos = []
        textos = []
        links = []
        page = Request('https://whitleyaward.org/category/news/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml') 
        soup2 = BeautifulSoup(str(soup.find_all('a', class_="sf-card__title-link")), 'lxml').get_text() # índice de notícias da página principal 


        for link in soup.find_all('a', class_="sf-card__title-link", href = True):
            links.append(link['href'])
            
        for i in links:
            page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(page).read()
            soup = BeautifulSoup(page_request, 'lxml')
            texto = clean(soup.find('div', class_ = "sf-article-content__text").get_text())
            titulo = clean(soup.find('h1').get_text())
            textos.append(texto)
            titulos.append(titulo)
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'whitleyaward_')
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em whitleyaward2')

#whitleyaward2()