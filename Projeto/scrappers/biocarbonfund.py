#AB #

import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
import numpy as np
from collections import OrderedDict
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

def biocarbonfund2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\biocarbonfund_02.csv'
        titulos = []
        textos = []
        links = []
        lista = []
        page = Request('https://www.biocarbonfund-isfl.org/news', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('div', class_ = 'view-content')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = i['href']
            if info.startswith('/result-stories/'):
                new_info = ('https://www.biocarbonfund-isfl.org/' + info)
                links.append(new_info)

        lista = np.unique(links).tolist()

        new_links = getNewInfo(links_base, lista)

        if(new_links):
            for link in new_links:
                page = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1', class_ = 'news-detail views-field-title').get_text()
                texto = soup.find('div', class_ = 'views-field views-field-body').get_text()
                titulos.append(titulo)
                textos.append(clean(texto))  
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
    
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = new_links
        df['not_texto'] = textos
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'biocarbonfund_')
        df['atualizacao'] = [dia]*len(df.index)
       
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em biocarbonfund2')
        
#biocarbonfund2('.')

def biocarbonfund3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\biocarbonfund_03.csv'
        titulos = []
        textos = []
        links = ['https://www.biocarbonfund-isfl.org/who-we-are']

        page = Request(links[0], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('h2', class_ = 'block-title').get_text()
        texto = soup.find('div', class_ = 'region region-content').get_text()
        titulos.append(titulo)
        textos.append(clean(texto))
        #print(textos)

        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['biocarbonfund'] * len(df.index)
        df['pol_texto'] = textos 
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'biocarbonfund_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em biocarbonfund3')
        
#biocarbonfund3('.')
