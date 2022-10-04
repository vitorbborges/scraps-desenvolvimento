#AB #112

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

def lindentrust3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\lindentrust_03.csv'
        titulos = []
        textos = []
        links = ['http://lindentrust.org/']

        page = Request('http://lindentrust.org/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('strong').get_text()
        texto = soup.find('article', class_ = 'post-4 page type-page status-publish hentry').get_text()
        titulos.append(titulo)
        textos.append(clean(texto))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['lindentrust']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'lindentrust_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em lindentrust3')
        
#lindentrust3('.')